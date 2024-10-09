import pytest
from panoramax_cli.status import get_uploadset_files
from panoramax_cli.exception import CliException
from panoramax_cli.model import UploadSet
import requests


def test_status_on_unknown_uploadset(panoramax):
    with pytest.raises(CliException) as e:
        with requests.session() as s:
            get_uploadset_files(panoramax, s, UploadSet(id="blabla"))

    assert e.match("Upload Set blabla not found")
