import functools
from typing import Callable, Any
import os
import sys
import re
import pathlib
import ast

__all__ = [
    "StatusCode",
    "Environment",
    "env",
    "failure",
    "success",
    "py_fnc",
    "sh_fnc",
    "to_snake_case",
    "to_kebab_case",
    "is_kebab_case",
    "is_snake_case",
    "is_lower_case",
    "is_camel_case",
    "is_pascal_case",
    "check_env",
    "parse_version",
    "generate_eggname",
    "expand_envvar_toml",
    "entrypoint_one_arg",
    "entrypoint_stdin",
]


class StatusCode:
    SUCCESS = 1
    FAILURE = 0


class Environment:
    def __init__(self):
        self._registry: dict[str, str] = {}

    def _register(self, varname: str) -> tuple[str, int]:
        (msg, ok) = check_env(varname)
        if not ok:
            return failure(msg)
        self._registry.update({varname: msg})
        return success(msg)

    def get(self, varname: str) -> str:
        value = self._registry.get(varname)
        if not value:
            raise RuntimeError(f"Unexpected runtime error for {varname=} lookup")
        return value

    def query(self, varname: str) -> tuple[str, int]:
        value = self._registry.get(varname)
        if not value:
            return self._register(varname)
        return success(value)

    def set(self, varname: str, value: str) -> tuple[str, int]:
        prev = self._registry.get(varname)
        if not prev or value != prev:
            self._registry.update({varname: value})
        return success(value)


env = Environment()

retval = lambda msg="", status=0: (msg, status)
failure = functools.partial(retval, status=StatusCode.FAILURE)
success = functools.partial(retval, status=StatusCode.SUCCESS)


match_kebab = re.compile(r"[\-]+[a-z0-9]*")
match_snake = re.compile(r"[\_]+[a-z0-9]*")
match_lower = re.compile(r"^[a-z0-9]+$")
match_envvar = re.compile(r"\$([A-Z_][A-Z0-9_]+)")


def py_fnc(fnc: Callable[[Any], tuple[str, int]]):
    def inner(*args, **kwargs) -> int:
        (msg, status) = fnc(*args, **kwargs)

        if msg:
            if status == StatusCode.SUCCESS:
                sys.stdout.write(msg)
            elif status == StatusCode.FAILURE:
                sys.stderr.write(msg)
        return not status

    return inner


def sh_fnc(fnc: Callable[[Any], tuple[str, int]]):
    def inner(*args, **kwargs) -> int:
        (msg, status) = fnc(*args, **kwargs)

        if msg:
            if status == StatusCode.FAILURE:
                sys.stdout.write(msg)
            elif status == StatusCode.SUCCESS:
                sys.stderr.write(msg)
        return status

    return inner


def to_snake_case(s: str) -> tuple[str, int]:
    return success("_".join(s.split("-")))


def to_kebab_case(s: str) -> tuple[str, int]:
    return success("-".join(s.split("_")))


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
    usage: parse_version [/path/to/version/file.py]
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
            node.value.value  # type: ignore
            for node in candidates
            if node.targets[0].id == "__version__"  # type: ignore
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


def expand_envvar_toml(s: str) -> tuple[str, int]:
    while m := match_envvar.search(s):
        a, b = m.span()
        # TODO: check_env
        val = os.getenv(m.group(1))

        if not val:
            return failure(f"{val} is not defined")
        s = s[:a] + val + s[b:]
    return success(s)


def _parse_version() -> int:
    """
    parse_version [/path/to/version/file]
    """
    if len(sys.argv) == 1:
        (workspace, ok) = check_env("WORKSPACE")
        if not ok:
            return py_fnc(failure)(workspace)
        (project_name, ok) = check_env("PROJECT_NAME")
        if not ok:
            return py_fnc(failure)(project_name)
        path = pathlib.Path(workspace) / project_name / "__init__.py"
        sys.argv.append(str(path))
    return entrypoint_one_arg(parse_version)


def _is_snake_case() -> int:
    return entrypoint_one_arg(is_snake_case)


def _is_kebab_case() -> int:
    return entrypoint_one_arg(is_kebab_case)


def _is_lower_case() -> int:
    return entrypoint_one_arg(is_lower_case)


def _generate_eggname() -> int:
    return entrypoint_one_arg(generate_eggname)


def _expand_toml() -> int:
    return entrypoint_stdin(expand_envvar_toml)


def _to_snake_case() -> int:
    return entrypoint_one_arg(to_snake_case)


def _to_kebab_case() -> int:
    return entrypoint_one_arg(to_kebab_case)


def match_pairs(f1: str, f2: str) -> tuple[str, int]:
    with open(f1) as f:
        ref = {i for i in f.read().split("\n")}
    with open(f2) as f:
        cmp = f.read().split("\n")

    return success("\n".join([i for i in cmp if i in ref]))


def _match_pairs() -> int:
    fnc = match_pairs
    if len(sys.argv) != 3:
        return py_fnc(failure)(f"{fnc.__doc__}")

    return py_fnc(fnc)(*sys.argv[1:])


def editor(argv: list[str]) -> tuple[str, int]:
    import subprocess
    import shutil
    import shlex

    def is_available(name: str):
        return shutil.which(name) is not None

    env = os.environ.copy()
    if is_available("nvim"):
        env.update({"XDG_CONFIG_HOME": os.getenv("DOTFILES")})
        cmd = ["nvim", *argv]
    elif is_available("vim"):
        cmd = ["vim", *argv]
    elif is_available("vi"):
        cmd = ["vi", *argv]
    elif is_available("nano"):
        cmd = ["nano", *argv]
    else:
        return failure("No known editor is available")

    ret = subprocess.run(shlex.join(cmd), shell=True, env=env)
    return ("", ret.returncode)


def _editor() -> int:
    return sh_fnc(editor)(sys.argv[1:])


def resolve_path(s: str) -> tuple[str, int]:
    import pathlib

    path = pathlib.Path(s)
    if not path.exists():
        return failure()
    return success(str(path.resolve()))


def _resolve_path() -> int:
    return entrypoint_one_arg(resolve_path)


def entrypoint_one_arg(fnc: Callable[[str], tuple[str, int]]) -> int:
    if len(sys.argv) != 2:
        return py_fnc(failure)(f"{fnc.__doc__}")
    return py_fnc(fnc)(sys.argv[1])


def entrypoint_stdin(fnc: Callable[[str], tuple[str, int]]) -> int:
    raw = "".join(sys.stdin.readlines())
    if not raw:
        return py_fnc(failure)(f"{fnc.__doc__}")
    return py_fnc(fnc)(raw)
