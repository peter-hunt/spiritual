from math import ceil, floor
from numbers import Number


def frange(*args):
    if len(args) == 1:
        start = 0
        stop = args[0]
        step = 1
    elif len(args) in {2, 3}:
        start = args[0]
        stop = args[1]
        step = 1 if len(args) == 2 else args[2]
    else:
        raise TypeError(f'frange expected 1-3 arguments, got {len(args)}')

    num = start
    while num < stop:
        yield num
        num += step


def pf_ceil(x: Number, /) -> float:
    return ceil(x + 0.5) - 0.5


def pf_floor(x: Number, /) -> float:
    return floor(x - 0.5) + 0.5
