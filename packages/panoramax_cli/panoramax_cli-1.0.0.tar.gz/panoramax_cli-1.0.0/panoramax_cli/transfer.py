from panoramax_cli.model import Panoramax, UploadSet, UploadFile, UploadParameters
from pathlib import Path
from typing import Optional, List
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
    Future,
    wait,
    FIRST_COMPLETED,
)
import signal
import sys
import json
from tempfile import TemporaryDirectory
from panoramax_cli.auth import login
from panoramax_cli.exception import CliException
from panoramax_cli.download import (
    _get_collection_meta,
    _get_collection_items,
    _get_collection_location,
    Quality,
    PicToDownload,
    get_user_collections,
)
from panoramax_cli.upload import (
    create_upload_set,
    upload_single_file,
    complete_upload_set,
)
from panoramax_cli import USER_AGENT, utils
import requests
import os
from rich import print
from rich.console import Group
from rich.live import Live
from rich.markup import escape
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeRemainingColumn,
)


def transfer_picture(
    from_api: Panoramax,
    to_api: Panoramax,
    pic: PicToDownload,
    uploadSet: UploadSet,
    session: requests.Session,
    picture_request_timeout: float,
    tmp_path: Path,
):
    picName = f"{pic.id}.jpg"
    picPath = tmp_path / picName

    # set auth headers only for panoramax instance. Important since the picture url might be an external url,
    # like a s3 link where we don't want to set panoramax auth headers.
    auth_headers = (
        session.headers.get("Authorization")
        if pic.download_url.startswith(from_api.url)
        else None
    )

    # Download single picture
    with session.get(
        pic.download_url,
        allow_redirects=True,
        timeout=picture_request_timeout,
        stream=True,
        headers={"Authorization": auth_headers},
    ) as res_pic_dl:
        if not res_pic_dl.ok:
            raise CliException(
                f"Impossible to download picture {pic.download_url}",
                details=res_pic_dl.text,
            )
        with picPath.open("wb") as picFile:
            picFile.write(res_pic_dl.content)

    # Upload downloaded picture
    uploadFile = UploadFile(picPath)
    uploadRes = upload_single_file(
        to_api, session, uploadSet, uploadFile, uploadTimeout=picture_request_timeout
    )

    # Remove picture from filesystem
    os.unlink(picPath)

    # Process upload response
    if uploadRes.status_code >= 400 and uploadRes.status_code != 409:
        errText = uploadRes.text
        errDetails = None
        try:
            rjson = uploadRes.json()
            if rjson.get("message"):
                errText = rjson["message"]
            if rjson.get("details") and rjson["details"].get("error"):
                errDetails = rjson["details"]["error"]
        except requests.exceptions.JSONDecodeError as e:
            pass
        raise CliException(errText, errDetails)

    return True


def _pic_list_iter(from_api, from_collection, session):
    for pic in _get_collection_items(
        session, _get_collection_location(from_api, from_collection), Quality.hd
    ):
        yield pic


def transfer_collection(
    from_collection: str,
    from_api: Panoramax,
    to_api: Panoramax,
    session: requests.Session,
    picture_request_timeout: float,
    parallel_transfers: int,
) -> str:
    print(f'📷 Retrieving collection "{from_collection}" metadata')
    coll_meta = _get_collection_meta(from_api, from_collection, session)
    nb_items = coll_meta["stats:items"]["count"]
    pic_generator = _pic_list_iter(from_api, from_collection, session)

    with TemporaryDirectory(prefix="gvs_") as tmp_dir_str:
        tmp_path = Path(tmp_dir_str)

        print("📦 Creating collection on destination API")
        uploadSet = UploadSet(
            title=coll_meta.get("title"),
            path=tmp_path,
            parameters=UploadParameters(already_blurred=True),
        )
        create_upload_set(to_api, session, uploadSet, nb_items)

        transfer_progress = Progress(
            TextColumn("{task.description}"),
            BarColumn(),
            TimeRemainingColumn(),
            TextColumn("[{task.completed}/{task.total}]"),
        )
        transfer_task = transfer_progress.add_task(
            f"[green]🚀 Transferring pictures...",
            total=nb_items,
        )

        with (
            ThreadPoolExecutor(max_workers=parallel_transfers) as executor,
            Live(transfer_progress) as live_render,
        ):

            def shutdown_executor(executor, err=None):
                live_render.stop()
                if err:
                    print(f"❌ Something went wrong...\n{err}")
                else:
                    print("🛑 Stopping...")
                executor.shutdown(wait=True)
                sys.exit()

            signal.signal(signal.SIGINT, lambda sig, frame: shutdown_executor(executor))

            try:
                futures = set()
                for pic in pic_generator:
                    future = executor.submit(
                        transfer_picture,
                        from_api,
                        to_api,
                        pic,
                        uploadSet,
                        session,
                        picture_request_timeout,
                        tmp_path,
                    )
                    futures.add(future)

                    # Wait for one task to end
                    if len(futures) >= parallel_transfers:
                        done, futures = wait(futures, return_when=FIRST_COMPLETED)
                        for future in done:
                            transfer_progress.advance(transfer_task)
                            future.result()

                # Wait for all other tasks to end
                for future in as_completed(futures):
                    transfer_progress.advance(transfer_task)
                    future.result()

            except KeyboardInterrupt:
                shutdown_executor(executor)
            except Exception as e:
                shutdown_executor(executor, e)

        print(f'🌠 Collection "{from_collection}" completely transferred')
        return uploadSet.id  # type: ignore


def transfer_user(
    user: str,
    from_api: Panoramax,
    to_api: Panoramax,
    session: requests.Session,
    picture_request_timeout: float,
    parallel_transfers: int,
):
    usIds = []
    for coll_uuid in get_user_collections(session, from_api, user):
        print("")  # Spacing
        usId = transfer_collection(
            coll_uuid,
            from_api,
            to_api,
            session,
            picture_request_timeout,
            parallel_transfers,
        )
        usIds.append(usId)

    print(f"\n🌠 All collections transfered")
    return usIds


def transfer(
    from_api: Panoramax,
    to_api: Panoramax,
    from_user: Optional[str] = None,
    from_collection: Optional[str] = None,
    disable_cert_check: bool = False,
    picture_request_timeout: float = 60.0,
    parallel_transfers: int = 1,
) -> List[str]:
    if not (from_user or from_collection) or (from_user and from_collection):
        raise CliException("You must either provide a user ID or sequence ID")

    with utils.createSessionWithRetry(disable_cert_check) as s:
        # Check both from/to APIs
        utils.test_panoramax_url(s, from_api.url)
        utils.test_panoramax_url(s, to_api.url)

        if from_user == "me":
            if not login(s, from_api):
                raise CliException(
                    "🔁 Computer not authenticated yet, impossible to transfer your pictures, but you can try again the same transfer command after finalizing the login"
                )

        if not login(s, to_api):
            raise CliException(
                "🔁 Computer not authenticated yet, impossible to transfer your pictures, but you can try again the same transfer command after finalizing the login"
            )

        if from_user:
            usIds = transfer_user(
                from_user,
                from_api,
                to_api,
                session=s,
                picture_request_timeout=picture_request_timeout,
                parallel_transfers=parallel_transfers,
            )
            return usIds
        else:
            assert from_collection
            usId = transfer_collection(
                from_collection,
                from_api,
                to_api,
                session=s,
                picture_request_timeout=picture_request_timeout,
                parallel_transfers=parallel_transfers,
            )
            return [usId]
