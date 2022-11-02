from typing import Optional, Callable
import sys
import re


class StatusCode:
    SUCCESS = 1
    FAILURE = 0

    @classmethod
    def shell_mode(cls):
        StatusCode.FAILURE, StatusCode.SUCCESS = 1, 0

    @classmethod
    def default_mode(cls):
        StatusCode.FAILURE, StatusCode.SUCCESS = 0, 1

    def __init__(self, code: int):
        self.status = code

    def __call__(self, msg: Optional[str] = "") -> int:
        if msg:
            sys.stdout.write(f"{msg}\n")
        return self.status


match_kebab = re.compile(r"[\-]+[a-z0-9]*")
match_snake = re.compile(r"[\_]+[a-z0-9]*")
match_lower = re.compile(r"^[a-z0-9]+$")
success = StatusCode(StatusCode.SUCCESS)
failure = StatusCode(StatusCode.FAILURE)


def _is_kebab_case(s: str) -> int:
    if match_snake.search(s):
        return failure()
    elif match_kebab.search(s):
        return success()
    return failure()


def _is_snake_case(s: str) -> int:
    if match_kebab.search(s):
        return failure()
    elif match_snake.search(s):
        return success()
    return failure()


def _is_lower_case(s: str) -> int:
    # "^(?:(?!:hede).)*$"
    if match_snake.search(s):
        return failure()
    elif match_kebab.search(s):
        return failure()
    elif match_lower.search(s):
        return success()
    return failure()


def _is_camel_case(s: str) -> int:
    raise NotImplementedError(s)


def _is_pascal_case(s: str) -> int:
    raise NotImplementedError(s)


def is_snake_case() -> int:
    return entrypoint_one_arg(_is_snake_case)


def is_kebab_case() -> int:
    return entrypoint_one_arg(_is_kebab_case)


def is_lower_case() -> int:
    return entrypoint_one_arg(_is_lower_case)


def entrypoint_one_arg(fnc: Callable[[str], int]) -> int:
    StatusCode.shell_mode()
    if len(sys.argv) != 2:
        return failure(f"{fnc.__name__[1:]} requires one positional argument")
    return fnc(sys.argv[1])
