"""Generates random tests."""

from sys import *
from kg.generators import * ### @import
from formatter import * ### @import
from itertools import chain

@listify
def gen_random(rand, *args):
    # example:
    A, = map(int,args[:1])

    for s in range(-2, 2+1):
        for t in range(-2, 2+1):
            yield s, t

    yield 0, A
    yield 0, -A
    yield -A, 0
    yield -A, 0

    def gen_small():
        return rand.randint(3, 10)
    
    def gen_big():
        return rand.randint(A - A//3, A)
    
    for _ in range(5):
        for f in [gen_small, gen_big]:
            for g in [gen_small, gen_big]:
                yield f(), g()

if __name__ == '__main__':
    write_to_files(format_case, gen_random, *argv[1:])
