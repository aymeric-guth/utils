from typing import Callable
from functools import partial
import sys
import re


class StatusCode:
    SUCCESS = 1
    FAILURE = 0


retval = lambda msg="", status=0: (msg, status)
failure = partial(retval, status=StatusCode.FAILURE)
success = partial(retval, status=StatusCode.SUCCESS)


match_kebab = re.compile(r"[\-]+[a-z0-9]*")
match_snake = re.compile(r"[\_]+[a-z0-9]*")
match_lower = re.compile(r"^[a-z0-9]+$")


def sh_fnc(fnc: Callable[[str], tuple[str, int]]):
    def inner(s: str) -> int:
        msg, status = fnc(s)

        # print(msg, status)
        if msg:
            if status == StatusCode.SUCCESS:
                sys.stdout.write(msg)
            elif status == StatusCode.FAILURE:
                sys.stderr.write(msg)
        return status

    return inner


def _is_snake_case(s: str) -> tuple[str, int]:
    """
    s: str -> tuple[str, int]
    """
    if match_kebab.search(s):
        return failure()
    elif match_snake.search(s):
        return success()
    return failure()


def is_snake_case() -> int:
    return entrypoint_one_arg(_is_snake_case)


def entrypoint_one_arg(fnc: Callable[[str], tuple[str, int]]) -> int:
    if len(sys.argv) != 2:
        return sh_fnc(failure)(f"{fnc.__doc__}")
    return sh_fnc(fnc)(sys.argv[1])
