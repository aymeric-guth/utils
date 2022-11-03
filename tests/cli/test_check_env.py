import os
from unittest import mock

from utils.cli import check_env, StatusCode


@mock.patch.dict(os.environ, {"VAR": ""})
def test_check_env_failure():
    _, status = check_env("VAR")
    assert status == StatusCode.FAILURE


@mock.patch.dict(os.environ, {"VAR": "VALUE"})
def test_check_env_success():
    _, status = check_env("VAR")
    assert status == StatusCode.SUCCESS
