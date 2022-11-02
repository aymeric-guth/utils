from typing import Optional
import sys


SUCCESS = 1
FAILURE = 0


def failure(msg: Optional[str] = None) -> int:
    if msg:
        sys.stdout.write(f"{msg}\n")
    return FAILURE


def success(msg: Optional[str] = None) -> int:
    if msg:
        sys.stdout.write(f"{msg}\n")
    return SUCCESS
