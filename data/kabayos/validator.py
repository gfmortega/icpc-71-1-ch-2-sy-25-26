"""Checks whether the input file is valid."""

from sys import *
from kg.validators import * ### @import

bounds = {
    'n': 1 <= +Var <= 100,
    'k': 1 <= +Var <= 2000,
    'c': 1 <= +Var <= 1200,
}


@validator(bounds=bounds)
def validate(stream, *, lim):
    ... # write your validator here

    # example:
    [n, c, k] = stream.read.int(lim.n).space.int(lim.c).space.int(lim.k).eoln
    [stats] = stream.read.ints(n, lim.c).eoln.eof
    ensure(all(stat <= c for stat in stats))


if __name__ == '__main__':
    validate(stdin)
