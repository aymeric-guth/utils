import functools
from typing import Optional, Callable, Union
import os
import sys
import re
import pathlib
import ast


class StatusCode:
    SUCCESS = 1
    FAILURE = 0


retval = lambda msg="", status=0: (msg, status)
failure = functools.partial(retval, status=StatusCode.FAILURE)
success = functools.partial(retval, status=StatusCode.SUCCESS)


match_kebab = re.compile(r"[\-]+[a-z0-9]*")
match_snake = re.compile(r"[\_]+[a-z0-9]*")
match_lower = re.compile(r"^[a-z0-9]+$")


def sh_fnc(fnc: Callable[[str], tuple[str, int]]):
    def inner(s: str) -> int:
        msg, status = fnc(s)

        if msg:
            if status == StatusCode.SUCCESS:
                sys.stdout.write(msg)
            elif status == StatusCode.FAILURE:
                sys.stderr.write(msg)
        return not status

    return inner


def to_snake_case(s: str) -> str:
    return "_".join(s.split("-"))


def to_kebab_case(s: str) -> str:
    return "-".join(s.split("_"))


def is_kebab_case(s: str) -> tuple[str, int]:
    """
    s: str
    """
    if match_snake.search(s):
        return failure()
    elif match_kebab.search(s):
        return success()
    return failure()


def is_snake_case(s: str) -> tuple[str, int]:
    """
    s: str -> tuple[str, int]
    """
    if match_kebab.search(s):
        return failure()
    elif match_snake.search(s):
        return success()
    return failure()


def is_lower_case(s: str) -> tuple[str, int]:
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


def is_camel_case(s: str) -> tuple[str, int]:
    """
    s: str
    """
    raise NotImplementedError(s)


def is_pascal_case(s: str) -> tuple[str, int]:
    """
    s: str
    """
    raise NotImplementedError(s)


def check_env(varname: str) -> tuple[str, int]:
    var = os.getenv(varname)
    if not var:
        return failure(f"{varname} is not defined")
    return success(var)


def parse_version(path: str) -> tuple[str, int]:
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


def generate_eggname(suffix: str) -> tuple[str, int]:
    (workspace, ok) = check_env("WORKSPACE")
    if not ok:
        return failure(workspace)
    (project_name, ok) = check_env("PROJECT_NAME")
    if not ok:
        return failure(project_name)
    if is_lower_case(project_name) or is_snake_case(project_name):
        python_package = project_name
    elif is_kebab_case(project_name):
        python_package = to_snake_case(project_name)
    else:
        return failure("unsupported project name")
    (version, ok) = parse_version(
        str(pathlib.Path(workspace) / python_package / "__init__.py")
    )
    if not ok:
        return failure(version)
    return success(f"{project_name}-{version}-{suffix}")


def _is_snake_case() -> int:
    return entrypoint_one_arg(is_snake_case)


def _is_kebab_case() -> int:
    return entrypoint_one_arg(is_kebab_case)


def _is_lower_case() -> int:
    return entrypoint_one_arg(is_lower_case)


def _parse_version() -> int:
    return entrypoint_one_arg(parse_version)


def _generate_eggname() -> int:
    return entrypoint_one_arg(generate_eggname)


def entrypoint_one_arg(fnc: Callable[[str], tuple[str, int]]) -> int:
    if len(sys.argv) != 2:
        return sh_fnc(failure)(f"{fnc.__doc__}")
    return sh_fnc(fnc)(sys.argv[1])
