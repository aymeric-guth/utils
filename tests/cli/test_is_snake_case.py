import pytest

from utils.cli import is_snake_case, StatusCode
from tests.cli import common  # type: ignore


params = [
    pytest.param(common.s_snake1, StatusCode.SUCCESS, id=""),
    pytest.param(common.s_kebab1, StatusCode.FAILURE, id=""),
    pytest.param(common.s_lower1, StatusCode.FAILURE, id=""),
    pytest.param(common.s_lower2, StatusCode.FAILURE, id=""),
    pytest.param(common.f_lower1, StatusCode.FAILURE, id=""),
    pytest.param(common.f_both, StatusCode.FAILURE, id=""),
]


@pytest.mark.parametrize(("s", "expected"), params)
def test_is_snake_case(s, expected):
    _, status = is_snake_case(s)
    assert status == expected
