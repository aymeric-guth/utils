import pytest

from utils.cli import StatusCode


@pytest.fixture(autouse=True, scope="session")
def env_setup():
    StatusCode.SUCCESS = 1
    StatusCode.FAILURE = 0


def test_default():
    assert StatusCode.FAILURE == 0 and StatusCode.SUCCESS == 1


def test_default_mode():
    StatusCode.default_mode()
    assert StatusCode.FAILURE == 0 and StatusCode.SUCCESS == 1


def test_shell_mode():
    StatusCode.shell_mode()
    assert StatusCode.FAILURE == 1 and StatusCode.SUCCESS == 0
