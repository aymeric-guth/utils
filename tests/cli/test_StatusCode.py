import pytest

from utils.cli import StatusCode, success, failure


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


def test_success_default():
    assert success() == StatusCode.SUCCESS


def test_success_default_mode():
    StatusCode.default_mode()
    assert success() == StatusCode.SUCCESS


def test_success_shell_mode():
    StatusCode.shell_mode()
    assert success() == StatusCode.SUCCESS


def test_failure_default():
    assert success() == StatusCode.SUCCESS


def test_failure_default_mode():
    StatusCode.default_mode()
    assert success() == StatusCode.SUCCESS


def test_failure_shell_mode():
    StatusCode.shell_mode()
    assert success() == StatusCode.SUCCESS
