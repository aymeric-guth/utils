import pytest

from utils.cli import StatusCode


@pytest.fixture(autouse=True, scope="session")
def env_setup():
    StatusCode.SUCCESS = 1
    StatusCode.FAILURE = 0
