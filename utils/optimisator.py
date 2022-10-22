#!/usr/bin/env python3
import time, re
from functools import wraps


class Time(object):
    def __init__(self, fnc):
        self.name = fnc.__name__
        self.calls = 0
        self.values = []
        self.total = 0

    def get_total(self):
        for i in self.values:
            self.total += i

def timer(fnc):
    @wraps(fnc)
    def inner(*args):
        t = args[0]
        start = time.time()
        if len(args) == 2:
            result = fnc(args[1])
        else:
            result = fnc(args[1], args[2])
        t.calls += 1
        t.values.append( time.time() - start )
        return result
    return inner


test_set = set( (1,) )

s = ".test1010 essai 123.lol"
X = 10000000
start = time.time()
for i in range(X):
#    s[0] != "."
#    "." not in s[0]
    s.startswith(".")

print(time.time() - start)
