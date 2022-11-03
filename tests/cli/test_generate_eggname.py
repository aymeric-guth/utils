import os
from unittest import mock

import pytest

from utils.cli import generate_eggname, StatusCode


suffix = "py3-none-any.whl"


@mock.patch.dict(os.environ, {"WORKSPACE": ""})
def test_generate_eggname_env_workspace_undefined():
    _, status = generate_eggname(suffix)
    assert status == StatusCode.FAILURE


@mock.patch.dict(os.environ, {"WORKSPACE": "value", "PROJECT_NAME": ""})
def test_generate_eggname_env_project_name_undefined():
    _, status = generate_eggname(suffix)
    assert status == StatusCode.FAILURE
