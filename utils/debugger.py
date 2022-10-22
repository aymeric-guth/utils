#!/usr/bin/env python3
from functools import wraps


class Debugger(type):
    """
    simple print base wrapper for instance methods
    adds call and return print for each method call
    metaclass applies debug decorator to all mathods
    """

    def __new__(cls, name, bases, attrs):
        # adds decorators to all methods except __methods__
        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and not (
                attr_name[:2] == "__" and attr_name[-2:] == "__"
            ):
                attrs.update({attr_name: Debugger.print_wrapper(attr_value)})

        return super().__new__(cls, name, bases, attrs)

    @staticmethod
    def print_wrapper(fnc):
        @wraps(fnc)
        def inner(*args, **kwargs):
            try:
                res = fnc(*args, **kwargs)
                print(f"{fnc.__name__} returned: {res}")
                return res
            except Exception as err:
                print(f"{fnc.__name__} exception occured: \n{err}")

        return inner


if __name__ == "__main__":
    """
    test code
    """

    class Base(metaclass=Debugger):
        def __init__(self):
            self.x = 10
            pass

        def meth01(self, x: int):
            pass

        def meth02(self, s: str):
            pass

        def meth03(self, f: float):
            return 1

        def __test__(self):
            pass

    b = Base()
    for n in range(10000):
        b.meth01(1)
        b.meth02("1")
        b.meth03(0.1)
    b.get_stats()
