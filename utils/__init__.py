from typing import Callable, Any, Union

from .config import Config
from . import cli
from . import fnc


__version__ = "0.0.7"

__all__ = [
    "Config",
    "cli",
    "fnc",
    "clamp",
    "to_snake_case",
    "to_kebab_case",
    "SingletonMeta",
    "try_not",
    "ascii_int",
    "lin_intp",
    "_lin_intp",
]



def clamp(lo: Union[int, float], hi: Union[int, float]) -> Callable[[Union[int, float]], Union[int, float]]:
    def inner(val: Union[int, float]) -> Union[int, float]:
        return max(lo, min(val, hi))

    return inner


def to_snake_case(s: str) -> str:
    return "_".join(s.split("-"))


def to_kebab_case(s: str) -> str:
    return "-".join(s.split("_"))


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


def try_not(fnc, exc) -> Callable:
    def inner(*args, **kwargs) -> None:
        try:
            fnc(*args, **kwargs)
        except exc:
            ...

    return inner


def ascii_int(b: bytes) -> int:
    """conversion ascii-encoded bytes -> int"""
    try:
        return int(b.decode("ascii"))
    except (ValueError, UnicodeError):
        return 0


def lin_intp(v: int, xa: int, ya: int, xb: int, yb: int) -> int:
    return (v - xa) * (yb - xb) // (ya - xa) + xb


def _lin_intp(xa: int, ya: int, xb: int, yb: int) -> Callable[[int], int]:
    def inner(v: int):
        return (v - xa) * (yb - xb) // (ya - xa) + xb

    return inner


def default_exc(fnc: Callable[[Any], Any], default: Any) -> Callable:
    def inner(*args, **kwargs) -> Any:
        try:
            return fnc(*args, **kwargs)
        except Exception:
            return default

    return inner


def default_null(fnc: Callable[[Any], Any], default: Any) -> Callable:
    def inner(*args, **kwargs) -> Any:
        retval = fnc(*args, **kwargs)
        if retval is None:
            return default
        return retval

    return inner
