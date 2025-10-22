"""Checks whether the input file is valid."""

from sys import *
from kg.validators import * ### @import

bounds = {
    'n': 1 <= +Var <= 100,
    'x': set('IJLOSTZ'),
}


@validator(bounds=bounds)
def validate(stream, *, lim):
    ... # write your validator here

    # example:
    [s] = stream.read.token(charset=lim.x).eoln.eof
    ensure(len(s) in lim.n)



if __name__ == '__main__':
    validate(stdin)
