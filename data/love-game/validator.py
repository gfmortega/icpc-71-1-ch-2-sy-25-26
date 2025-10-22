"""Checks whether the input file is valid."""

from sys import *
from kg.validators import * ### @import

bounds = {
    'x': -10**9 <= +Var <= 10**9,
}


@validator(bounds=bounds)
def validate(stream, *, lim):
    ... # write your validator here

    # example:
    [s, t] = stream.read.int(lim.x).space.int(lim.x).eoln.eof


if __name__ == '__main__':
    validate(stdin)
