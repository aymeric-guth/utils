import time
from collections import defaultdict
from functools import wraps


class Timer(object):
    def __init__(self, name):
        self.name = name
        self.calls = 0
        self.values = []
        self.buffer = 0
        self.total = 0

    def __str__(self):
        if not (self.total):
            return f"{self.name}:\nTook: {self.get_total()}\nCalls: {self.calls}"
        else:
            return f"{self.name}:\nTook: {self.total}\nCalls: {self.calls}"

    def get_total(self, offset=0):
        return sum(self.values) - 0

    def start(self):
        self.buffer = time.time()
        self.calls += 1

    def stop(self):
        self.values.append(time.time() - self.buffer)


class Time(object):
    def __init__(self):
        self.resutls = {}
        self.call_order = []
        self.length = 0

    def add(self, name):
        if name not in self.resutls:
            self.call_order.append(name)
            self.resutls[name] = Timer(name)
            self.length += 1

        return self.resutls[name]

    def re_init(self):
        self.resutls = {}
        self.call_order = []
        self.length = 0

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < self.length:
            value = self.resutls[self.call_order[self.n]]
            self.n += 1
            return value
        else:
            raise StopIteration

    def __str__(self):
        value = self.resutls[self.call_order[self.n]]
        return value.__str__()


def timer(fnc):
    @wraps(fnc)
    def inner(*args, **kwargs):
        global results

        t = results.add(fnc.__name__)
        t.start()
        result = fnc(*args, **kwargs)
        t.stop()
        return result

    return inner


def timer_(fnc):
    @wraps(fnc)
    def inner(*args, **kwargs):
        args = (*args, True)
        return fnc(*args, **kwargs)

    return inner


results = Time()
