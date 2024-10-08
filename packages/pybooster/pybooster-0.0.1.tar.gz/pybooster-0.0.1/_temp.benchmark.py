# ruff: noqa: S101,T201

import statistics
import timeit
from typing import NewType

from pybooster import injector
from pybooster import provider
from pybooster import required
from pybooster import shared

MyStr = NewType("MyStr", str)

VAL = MyStr("")


@provider.function
def string() -> MyStr:
    return VAL


def control_context():
    with string.value() as value:
        assert value == VAL


def _control_call(s):
    assert s == VAL


def control_call():
    _control_call(s=VAL)


@injector.function
def use_string(*, s: MyStr = required):
    assert s == VAL


def timings(func, *args, **kwargs):
    timer = timeit.Timer("main()", globals={"main": lambda: func(*args, **kwargs)})
    number, _ = timer.autorange()
    timings = [t / number for t in timer.repeat(repeat=10, number=number)]
    return {
        "best": min(timings),
        "mean": statistics.mean(timings),
        "stdev": statistics.stdev(timings),
    }


if __name__ == "__main__":
    with string.scope():
        print("Explicit:       ", timings(use_string, s=""))

    with string.scope(), shared(MyStr):
        print("Singleton:    ", timings(use_string))

    with string.scope():
        print("Default:  ", timings(use_string))

    print("Control:", timings(control_context))
