import pytest

from utils.cli import _is_lower_case, StatusCode
from tests.cli import common  # type: ignore


@pytest.fixture(autouse=True, scope="session")
def env_setup():
    StatusCode.default_mode()


params = [
    pytest.param(common.s_snake1, StatusCode.FAILURE, id=""),
    pytest.param(common.s_kebab1, StatusCode.FAILURE, id=""),
    pytest.param(common.s_lower1, StatusCode.SUCCESS, id=""),
    pytest.param(common.s_lower2, StatusCode.SUCCESS, id=""),
    pytest.param(common.f_lower1, StatusCode.FAILURE, id=""),
    pytest.param(common.f_both, StatusCode.FAILURE, id=""),
]


@pytest.mark.parametrize(("s", "expected"), params)
def test_is_lower_case(s, expected):
    assert _is_lower_case(s) == expected
