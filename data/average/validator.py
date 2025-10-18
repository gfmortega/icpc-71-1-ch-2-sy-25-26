"""Checks whether the input file is valid."""

from sys import *
from kg.validators import * ### @import

bounds = {
    'n': 1 <= +Var <= 60,
    'a': 0 <= +Var <= 100,
}


@validator(bounds=bounds)
def validate(stream, *, lim):
    ... # write your validator here

    # example:
    [[n, k]] = stream.read.ints(2, lim.n).eoln
    ensure(k < n)
    [a] = stream.read.ints(n, lim.a).eoln.eof



if __name__ == '__main__':
    validate(stdin)
