from typing import Optional, Callable
import sys
import re
import pathlib
import ast


class StatusCode:
    SUCCESS = 1
    FAILURE = 0

    @classmethod
    def shell_mode(cls):
        StatusCode.FAILURE, StatusCode.SUCCESS = 1, 0

    @classmethod
    def default_mode(cls):
        StatusCode.FAILURE, StatusCode.SUCCESS = 0, 1

    @classmethod
    def msg(cls, msg: Optional[str] = "") -> None:
        if msg:
            sys.stdout.write(f"{msg}\n")

    @classmethod
    def success(cls, msg: Optional[str] = "") -> int:
        StatusCode.msg(msg)
        return StatusCode.SUCCESS

    @classmethod
    def failure(cls, msg: Optional[str] = "") -> int:
        StatusCode.msg(msg)
        return StatusCode.FAILURE


match_kebab = re.compile(r"[\-]+[a-z0-9]*")
match_snake = re.compile(r"[\_]+[a-z0-9]*")
match_lower = re.compile(r"^[a-z0-9]+$")
success = StatusCode.success
failure = StatusCode.failure


def _is_kebab_case(s: str) -> int:
    """
    s: str
    """
    if match_snake.search(s):
        return failure()
    elif match_kebab.search(s):
        return success()
    return failure()


def _is_snake_case(s: str) -> int:
    """
    s: str
    """
    if match_kebab.search(s):
        return failure()
    elif match_snake.search(s):
        return success()
    return failure()


def _is_lower_case(s: str) -> int:
    """
    s: str
    """
    # "^(?:(?!:hede).)*$"
    if match_snake.search(s):
        return failure()
    elif match_kebab.search(s):
        return failure()
    elif match_lower.search(s):
        return success()
    return failure()


def _is_camel_case(s: str) -> int:
    """
    s: str
    """
    raise NotImplementedError(s)


def _is_pascal_case(s: str) -> int:
    """
    s: str
    """
    raise NotImplementedError(s)


def is_snake_case() -> int:
    return entrypoint_one_arg(_is_snake_case)


def is_kebab_case() -> int:
    return entrypoint_one_arg(_is_kebab_case)


def is_lower_case() -> int:
    return entrypoint_one_arg(_is_lower_case)


def _parse_version(path: str) -> int:
    """
    usage: parse_version /path/to/version/file
    """
    p = pathlib.Path(path).resolve()
    if p.suffix != ".py":
        return failure(f"extension {p.suffix} not supported")
    if not p.exists():
        return failure("version file does not exists")
    tree = ast.parse(p.read_text())
    candidates = [node for node in tree.body if isinstance(node, ast.Assign)]
    if not candidates:
        return failure(f"could not find a suitable node in {p!s}")
    try:
        version = [
            node.value.value
            for node in candidates
            if node.targets[0].id == "__version__"
        ]
    except Exception as e:
        return failure(f"unexpected error: {e}")
    if not version:
        return failure(f"could not find version in {p!s}")
    if len(version) > 1:
        return failure(f"got multiple versions for file {p!s}")
    return success(version[0])


def parse_version() -> int:
    return entrypoint_one_arg(_parse_version)


def entrypoint_one_arg(fnc: Callable[[str], int]) -> int:
    StatusCode.shell_mode()
    if len(sys.argv) != 2:
        return failure(f"{fnc.__doc__}")
    return fnc(sys.argv[1])
