"""Checks whether the input file is valid."""

from sys import *
from kg.validators import * ### @import

bounds = {
    'n': 2 <= +Var <= 100,
    'v': 1 <= +Var <= 100,
}


@validator(bounds=bounds)
def validate(stream, *, lim):
    ... # write your validator here

    # example:
    [n] = stream.read.int(lim.n).eoln
    [a, c] = stream.read.ints(n, lim.v).eoln.ints(n, lim.v).eoln.eof

    for arr in [a, c]:
        ensure(all(1 <= x <= n for x in arr))
        ensure(len(arr) == len(set(arr)) == n)



if __name__ == '__main__':
    validate(stdin)
