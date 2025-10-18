"""Checks whether the input file is valid."""

from sys import *
from kg.validators import * ### @import

bounds = {
    'n': 1 <= +Var <= 100,
    'a': 2 <= +Var <= 1000,
}


@validator(bounds=bounds)
def validate(stream, *, lim):
    ... # write your validator here

    # example:
    [n, k] = stream.read.int(lim.n).space.int(lim.a).eoln
    [a] = stream.read.ints(n, lim.a).eoln.eof



if __name__ == '__main__':
    validate(stdin)
