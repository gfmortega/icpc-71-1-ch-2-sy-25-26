"""Generates random tests."""

from sys import *
from kg.generators import * ### @import
from formatter import * ### @import
from itertools import chain

@listify
def gen_random(rand, *args):
    # example:
    N, = map(int,args[:1])

    yield [1, 2], [2, 1]

    asc = list(range(1, N+1))
    dec = list(reversed(asc))
    yield asc, asc
    yield asc, dec
    yield dec, asc
    yield dec, dec

    for _ in range(10):
        yield rand.shuffled(asc), rand.shuffled(dec)


if __name__ == '__main__':
    write_to_files(format_case, gen_random, *argv[1:])
