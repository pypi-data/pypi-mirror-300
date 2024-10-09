import os
import pytest
import requests
import panoramax_cli.exception
import panoramax_cli.model
import panoramax_cli.status
import panoramax_cli.upload
import panoramax_cli.transfer
from tests.conftest import FIXTURE_DIR
from pathlib import Path
import shutil

from tests.integration.conftest import cleanup_panoramax, login


@pytest.fixture
def load_data(panoramax_with_token, tmpdir_factory):
    import tempfile

    # do not use tmp_path since we want to use it as a fixture module
    tmp_dir = Path(tempfile.gettempdir())
    fixture_dir = Path(FIXTURE_DIR)

    tmp_dir = Path(tmpdir_factory.mktemp("panoramax_data"))

    dir1 = tmp_dir / "collection1"
    dir1.mkdir()
    dir2 = tmp_dir / "collection2"
    dir2.mkdir()
    shutil.copy(fixture_dir / "e1.jpg", dir1 / "e1.jpg")
    shutil.copy(fixture_dir / "e2.jpg", dir1 / "e2.jpg")
    shutil.copy(fixture_dir / "e3.jpg", dir2 / "e3.jpg")
    cleanup_panoramax(panoramax_with_token)

    uploadReport = panoramax_cli.upload.upload_path(
        path=tmp_dir,
        panoramax=panoramax_with_token,
        uploadTimeout=20,
        wait=True,
        title=None,
    )
    assert len(uploadReport.uploaded_files) == 3
    assert len(uploadReport.upload_sets) == 2
    assert len(uploadReport.upload_sets[0].associated_collections) == 1
    assert len(uploadReport.upload_sets[1].associated_collections) == 1
    return uploadReport


def test_valid_collection_transfer(panoramax_with_token, user_credential, load_data):
    with requests.session() as s:
        login(s, panoramax_with_token, user_credential)
        usid = panoramax_cli.transfer.transfer_collection(
            from_collection=load_data.upload_sets[0].associated_collections[0].id,
            from_api=panoramax_with_token,
            to_api=panoramax_with_token,
            session=s,
            picture_request_timeout=20,
            parallel_transfers=1,
        )
        panoramax_cli.status.wait_for_upload_sets(
            panoramax_with_token, s, [panoramax_cli.model.UploadSet(id=usid)]
        )
        us = panoramax_cli.status.get_uploadset_files(
            panoramax_with_token, s, panoramax_cli.model.UploadSet(id=usid)
        )
        assert len(us.files) > 0


def test_valid_user_me_transfer(panoramax_with_token, load_data, user_credential):
    usIds = panoramax_cli.transfer.transfer(
        from_api=panoramax_with_token,
        to_api=panoramax_with_token,
        from_user="me",
    )

    with requests.session() as s:
        panoramax_cli.status.wait_for_upload_sets(
            panoramax_with_token,
            s,
            [panoramax_cli.model.UploadSet(id=u) for u in usIds],
        )
        login(s, panoramax_with_token, user_credential)
        us = [
            panoramax_cli.status.get_uploadset_files(
                panoramax_with_token, s, panoramax_cli.model.UploadSet(id=usid)
            )
            for usid in usIds
        ]
        assert len(us) == 2
        assert sum([len(u.files) for u in us]) == 3


def test_invalid_user_id_transfer(panoramax_with_token, load_data):
    with pytest.raises(panoramax_cli.exception.CliException) as e:
        panoramax_cli.transfer.transfer(
            from_api=panoramax_with_token,
            to_api=panoramax_with_token,
            from_user="prout",
        )
    assert str(e.value).startswith("Impossible to find user prout")


def test_invalid_collection_id_transfer(panoramax_with_token, load_data):
    with pytest.raises(panoramax_cli.exception.CliException) as e:
        panoramax_cli.transfer.transfer(
            from_api=panoramax_with_token,
            to_api=panoramax_with_token,
            from_collection="prout",
        )
    assert str(e.value).startswith("Impossible to get collection prout"), e.value


def test_valid_user_id_transfer(panoramax_with_token, load_data, user_credential):
    user = requests.get(f"{panoramax_with_token.url}/api/users")
    user.raise_for_status()
    user_id = next(u["id"] for u in user.json()["users"] if u["name"] == "elysee")

    usIds = panoramax_cli.transfer.transfer(
        from_api=panoramax_with_token,
        to_api=panoramax_with_token,
        from_user=user_id,
    )

    with requests.session() as s:
        panoramax_cli.status.wait_for_upload_sets(
            panoramax_with_token,
            s,
            [panoramax_cli.model.UploadSet(id=u) for u in usIds],
        )
        login(s, panoramax_with_token, user_credential)
        us = [
            panoramax_cli.status.get_uploadset_files(
                panoramax_with_token, s, panoramax_cli.model.UploadSet(id=usid)
            )
            for usid in usIds
        ]
        assert len(us) == 2
        assert sum([len(u.files) for u in us]) == 3
