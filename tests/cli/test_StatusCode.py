import pytest

from utils.cli import StatusCode, success, failure, sh_fnc


test_msg = "test"


def test_default():
    assert StatusCode.FAILURE == 0 and StatusCode.SUCCESS == 1


def test_unit_failure_default():
    msg, status = failure()
    assert msg == "" and status == StatusCode.FAILURE


def test_unit_failure_msg():
    msg, status = failure(test_msg)
    assert msg == test_msg and status == StatusCode.FAILURE


def test_unit_success_default():
    msg, status = success()
    assert msg == "" and status == StatusCode.SUCCESS


def test_unit_success_msg():
    msg, status = success(test_msg)
    assert msg == test_msg and status == StatusCode.SUCCESS


def test_sh_fnc_failure():
    assert sh_fnc(success)("") == StatusCode.FAILURE


def test_sh_fnc_success():
    assert sh_fnc(failure)("") == StatusCode.SUCCESS
