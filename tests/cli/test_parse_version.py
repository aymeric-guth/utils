import pathlib
import shutil
import os

import pytest

from utils.cli import parse_version, StatusCode


root = pathlib.Path(__file__).parent
env_root = root / "env"


@pytest.fixture(autouse=True, scope="session")
def env_setup():
    try:
        os.makedirs(env_root)
    except OSError:
        shutil.rmtree(env_root)
        os.makedirs(env_root)
    yield
    try:
        shutil.rmtree(env_root)
    except OSError:
        ...


def test_parse_version_path_invalid():
    arg = str(env_root / "file.py")
    _, status = parse_version(arg)
    assert status == StatusCode.FAILURE


def test_parse_version_invalid_file():
    f = env_root / "file.file"
    f.touch()
    arg = str(f)
    _, status = parse_version(arg)
    assert status == StatusCode.FAILURE


def test_parse_version_no_assign_node():
    f = env_root / "file.py"
    f.write_text("import sys\n")
    arg = str(f)
    _, status = parse_version(arg)
    assert status == StatusCode.FAILURE


def test_parse_version_one_assign_node_with_version():
    f = env_root / "file.py"
    f.write_text("import sys\n__version__ = '0.0.0'\n")
    arg = str(f)
    _, status = parse_version(arg)
    assert status == StatusCode.SUCCESS


def test_parse_version_multiple_assign_node_with_version():
    f = env_root / "file.py"
    f.write_text("import sys\n__version__ = '0.0.0'\n__version__ = '1.0.0'\n")
    arg = str(f)
    _, status = parse_version(arg)
    assert status == StatusCode.FAILURE
