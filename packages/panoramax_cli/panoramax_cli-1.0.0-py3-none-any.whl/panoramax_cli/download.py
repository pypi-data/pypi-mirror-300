from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import string
import re
import requests
from typing import List, Dict, Optional
from rich import print
from rich.console import Group
from rich.live import Live
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from panoramax_cli import USER_AGENT, exception, utils
import json
from panoramax_cli.auth import login
from panoramax_cli.exception import CliException
from panoramax_cli.model import (
    Panoramax,
    FileName,
)


@dataclass
class PicToDownload:
    download_url: str
    original_size: int
    name: str
    id: str
    raw_response: Dict


class Quality(Enum):
    sd = "sd"
    hd = "hd"
    thumb = "thumb"


def get_collection_path(collection: Dict, path: Path) -> Path:
    punctuation = f"[{re.escape(string.punctuation)}]"
    whitespace = f"[{re.escape(string.whitespace)}]"
    title = collection["title"]
    folder_name = re.sub(whitespace, "_", re.sub(punctuation, "_", title))
    local_folder_path = path / f"{folder_name}"
    return local_folder_path


def _get_collection_location(panoramax: Panoramax, collection_id: str) -> str:
    return f"{panoramax.url}/api/collections/{collection_id}"


def _get_collection_meta(
    panoramax: Panoramax, collection_id: str, session: requests.Session
):
    collection_response = session.get(
        _get_collection_location(panoramax, collection_id)
    )
    if not collection_response.ok:
        if collection_response.status_code == "404":
            raise CliException(f"Impossible to find collection {collection_id}")
        raise CliException(
            f"Impossible to get collection {collection_id}",
            details=collection_response.text,
        )

    collection = collection_response.json()
    return collection


def _get_collection_items(
    session: requests.Session, col_location: str, quality: Quality
):
    url: Optional[str] = f"{col_location}/items?limit=500"
    while url:
        items_r = session.get(url)
        if not items_r:
            raise CliException(
                f"Impossible to get collection items", details=items_r.text
            )
        items = items_r.json()

        for item in items["features"]:
            asset = next(
                (
                    a
                    for k, a in item["assets"].items()
                    if k == quality.value and a["type"] == "image/jpeg"
                ),
                None,
            )
            if asset:
                yield PicToDownload(
                    download_url=asset["href"],
                    original_size=item["properties"].get("original_file:size"),
                    name=item["properties"]["original_file:name"],
                    id=item["id"],
                    raw_response=item,
                )
        url = next((l["href"] for l in items["links"] if l["rel"] == "next"), None)


def _download_collection(
    collection_id: str,
    panoramax: Panoramax,
    file_name: FileName,
    path: Path,
    picture_dl_timeout: float,
    session: requests.Session,
    quality: Quality,
    external_metadata_dir_name: Optional[Path] = None,
) -> None:
    downloading_progress = Progress(
        BarColumn(),
        TimeElapsedColumn(),
        TextColumn("[{task.completed}/{task.total}]"),
        "⏳",
        TimeRemainingColumn(compact=True),
        "remaining",
        TextColumn("[green]{task.fields[skipped_msg]}[/green]"),
    )
    current_pic_progress = Progress(
        TextColumn("{task.description}"),
        SpinnerColumn("simpleDots"),
    )
    progress_group = Group(
        downloading_progress,
        current_pic_progress,
    )

    # Strategy for filename
    if file_name not in [item.value for item in FileName]:
        raise exception.CliException("Invalid file-name strategy: " + str(file_name))

    # fetch download_url and names of pictures
    collection = _get_collection_meta(panoramax, collection_id, session)
    nb_items = collection["stats:items"]["count"]
    downloading_progress.console.print(
        f" [green]⬇️  Downloading sequence[/green] [bold]{collection['title']}[/bold] ({collection['id']})"
    )
    local_folder_path = get_collection_path(collection, path)
    # create folder if needed
    local_folder_path.mkdir(parents=True, exist_ok=True)
    external_metadata_path = (
        local_folder_path / external_metadata_dir_name
        if external_metadata_dir_name
        else None
    )
    if external_metadata_path:
        external_metadata_path.mkdir(parents=True, exist_ok=True)

    downloading_task = downloading_progress.add_task(
        "",
        total=nb_items,
        skipped_msg="",
    )
    downloading_progress.update(downloading_task)
    current_pic_task = current_pic_progress.add_task(
        f"  🔄 Retrieving collection's list of pictures"
    )
    pic_list = _get_collection_items(
        session, _get_collection_location(panoramax, collection_id), quality
    )

    nb_skipped = 0
    with Live(progress_group):
        for picToDownload in pic_list:
            name = (
                picToDownload.name
                if file_name == FileName.original_name
                else f"{picToDownload.id}.jpg"
            )
            local_picture_path = local_folder_path / name
            downloading_progress.advance(downloading_task)

            if external_metadata_path:
                # if external metadata is provided, persist the api response in a separate json file
                # always persist the response even if file is there, as it could have been updated on the server
                external_metadata_file = external_metadata_path / f"{name}.json"

                with external_metadata_file.open("wb") as response_file:
                    response_file.write(json.dumps(picToDownload.raw_response).encode())

            if local_picture_path.exists():
                # if local picture exists, skip the download.
                nb_skipped += 1
                downloading_progress.update(
                    downloading_task,
                    skipped_msg=f"({nb_skipped} pictures already downloaded, skipped)",
                )
                continue
            current_pic_progress.update(
                current_pic_task,
                description=f"  📷 Downloading [bold purple]{picToDownload.name}",
            )

            # set auth headers only for panoramax instance. Important since the picture url might be an external url,
            # like a s3 link where we don't want to set panoramax auth headers.
            auth_headers = (
                session.headers.get("Authorization")
                if picToDownload.download_url.startswith(panoramax.url)
                else None
            )

            with session.get(
                picToDownload.download_url,
                allow_redirects=True,
                timeout=picture_dl_timeout,
                stream=True,
                headers={"Authorization": auth_headers},
            ) as response_photo:
                if not response_photo.ok:
                    raise CliException(
                        f"Impossible to download picture {picToDownload.download_url}",
                        details=response_photo.text,
                    )
                with local_picture_path.open("wb") as photo_file:
                    photo_file.write(response_photo.content)
                # TODO check the size of the downloaded picture with picToDownload.original_size ?


def download_collection(
    collection_id: str,
    panoramax: Panoramax,
    session: requests.Session,
    file_name: FileName,
    path: Path = Path("."),
    picture_dl_timeout: float = 60.0,
    external_metadata_dir_name: Optional[Path] = None,
    quality: Quality = Quality.hd,
) -> None:
    path.mkdir(parents=True, exist_ok=True)
    if not path.is_dir():
        raise CliException(f"{path} is not a directory, cannot download pictures")

    _download_collection(
        collection_id=collection_id,
        panoramax=panoramax,
        path=path,
        session=session,
        file_name=file_name,
        picture_dl_timeout=picture_dl_timeout,
        external_metadata_dir_name=external_metadata_dir_name,
        quality=quality,
    )


def get_user_collections(session, panoramax: Panoramax, user_id: str):
    user_url: Optional[str] = f"{panoramax.url}/api/users/{user_id}/collection"

    first_page = True
    while user_url:
        r = session.get(user_url)
        if not r.ok:
            if r.status_code == 404:
                raise CliException(f"Impossible to find user {user_id}")
            raise CliException(
                f"Impossible to query user {user_url} collections", details=r.text
            )
        dict_coll = r.json()
        title = dict_coll["title"]
        nb_pictures = dict_coll["stats:items"]["count"]
        if first_page:
            nb_sequences = dict_coll.get("stats:collections", {}).get("count")

            print(
                f"👥 Downloading {title}: {nb_pictures} pictures{' on {nb_sequences} collections' if nb_sequences else ''}"
            )
            first_page = False

        for link in dict_coll["links"]:
            if link["rel"] == "child":
                coll_uuid = link["href"].split("/")[-1]
                yield coll_uuid

        user_url = next(
            (l["href"] for l in dict_coll["links"] if l["rel"] == "next"), None
        )


def download_user(
    user_id: str,
    panoramax: Panoramax,
    file_name: FileName,
    session: requests.Session,
    path: Path = Path("."),
    picture_dl_timeout: float = 60.0,
    external_metadata_dir_name: Optional[Path] = None,
    quality: Quality = Quality.hd,
) -> None:
    # create folder
    path.mkdir(parents=True, exist_ok=True)
    if not path.is_dir():
        raise CliException(f"{path} is not a directory, cannot download pictures")

    for coll_uuid in get_user_collections(session, panoramax, user_id):
        download_collection(
            coll_uuid,
            panoramax,
            session=session,
            file_name=file_name,
            path=path,
            picture_dl_timeout=picture_dl_timeout,
            external_metadata_dir_name=external_metadata_dir_name,
            quality=quality,
        )


def download(
    panoramax: Panoramax,
    user: Optional[str] = None,
    collection: Optional[str] = None,
    file_name: FileName = FileName.original_name,
    path: Path = Path("."),
    disable_cert_check: bool = False,
    picture_dl_timeout: float = 60.0,
    external_metadata_dir_name: Optional[Path] = None,
    quality: Quality = Quality.hd,
) -> None:
    if not (user or collection) or (user and collection):
        raise exception.CliException("provide a user id OR a sequence id")
    with utils.createSessionWithRetry(disable_cert_check) as s:
        utils.test_panoramax_url(s, panoramax.url)
        if user == "me":
            if not login(s, panoramax):
                raise exception.CliException(
                    "🔁 Computer not authenticated yet, impossible to download your pictures, but you can try again the same download command after finalizing the login"
                )

        if user:
            download_user(
                user,
                panoramax,
                session=s,
                path=path,
                file_name=file_name,
                picture_dl_timeout=picture_dl_timeout,
                external_metadata_dir_name=external_metadata_dir_name,
                quality=quality,
            )
        else:
            assert collection
            download_collection(
                collection,
                panoramax,
                session=s,
                path=path,
                file_name=file_name,
                picture_dl_timeout=picture_dl_timeout,
                external_metadata_dir_name=external_metadata_dir_name,
                quality=quality,
            )
