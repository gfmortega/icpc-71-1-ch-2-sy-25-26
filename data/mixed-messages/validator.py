"""Checks whether the input file is valid."""

from sys import *
from kg.validators import * ### @import

bounds = {
    'n': 1 <= +Var <= 100,
    'charset': set('23456789'),
}


@validator(bounds=bounds)
def validate(stream, *, lim):
    ... # write your validator here

    # example:
    [s] = stream.read.token(charset=lim.charset).eoln.eof
    ensure(len(s) in lim.n)


if __name__ == '__main__':
    validate(stdin)
