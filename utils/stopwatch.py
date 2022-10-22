#!/usr/bin/env python3
from functools import wraps
import time


class Stopwatch(type):
    """
    profiling meta, adds stopwatch wrappers to all non __ methods
    and specific statistics methods for results
    """

    def __new__(cls, name, bases, attrs):
        observable_meth = []
        # adds decorators to all methods except __methods__
        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and not (
                attr_name[:2] == "__" and attr_name[-2:] == "__"
            ):
                attrs.update({attr_name: Stopwatch.timer(attr_value)})
                observable_meth.append(attr_name)

        # adds statistics method
        attrs.update({"get_stats": Stopwatch.get_stats})
        instance = super().__new__(cls, name, bases, attrs)

        # adds stopwatch per method attributes
        setattr(instance, "observable_meth", observable_meth)
        for meth_name in observable_meth:
            setattr(instance, f"{meth_name}_timer", [])
            setattr(instance, f"{meth_name}_calls", 0)

        return instance

    @staticmethod
    def timer(fnc):
        @wraps(fnc)
        def inner(*args, **kwargs):
            self, *_ = args
            value = getattr(self, f"{fnc.__name__}_calls")
            setattr(self, f"{fnc.__name__}_calls", value + 1)
            start = time.time()
            result = fnc(*args, **kwargs)
            value = getattr(self, f"{fnc.__name__}_timer")
            value.append(time.time() - start)
            return result

        return inner

    @staticmethod
    def get_stats(self):
        for meth_name in self.observable_meth:
            calls = getattr(self, f"{meth_name}_calls")
            if not calls:
                continue
            chrono = getattr(self, f"{meth_name}_timer")
            avg = sum(chrono) / len(chrono)
            print(
                f"{meth_name}: calls: {calls} total: {sum(chrono)} average: {avg} min: {min(chrono)} max: {max(chrono)}"
            )


if __name__ == "__main__":
    """test code"""
    # import cProfile
    # import pstats
    # with cProfile.Profile() as pr:
    #   fnc()
    # stats = pstats.Stats(pr)
    # stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()
    # stats.dump_stats(filename='profile.prof')

    # snakewiz
    class Base(metaclass=Stopwatch):
        def __init__(self):
            self.x = 10
            pass

        def meth01(self, x: int):
            pass

        def meth02(self, s: str):
            pass

        def meth03(self, f: float):
            pass

        def __test__(self):
            pass

    b = Base()
    for n in range(10000):
        b.meth01(1)
        b.meth02("1")
        b.meth03(0.1)
    b.get_stats()
