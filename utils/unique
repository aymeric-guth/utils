#!/usr/bin/env python3
import sys

# import os.path
import pathlib


def main(argv: list[str]) -> int:
    dirs = []
    for item in argv:
        p = pathlib.Path(item[:-1])
        if not p.exists():
            continue
        if p.is_dir():
            dirs.append(str(p))
        else:
            dirs.append(str(p.parent))
    l = list(set(dirs))
    l.sort(reverse=True)
    sys.stdout.write("\n".join(l))
    return 0


if __name__ == "__main__":
    argv = [i for i in sys.stdin]
    if argv:
        sys.exit(main(argv))
