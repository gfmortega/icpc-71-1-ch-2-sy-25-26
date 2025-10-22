"""Generates random tests."""

from sys import *
from kg.generators import * ### @import
from formatter import * ### @import
from itertools import chain

@listify
def gen_random(rand, *args):
    # example:
    N, = map(int,args[:1])

    DIGITS = '23456789'
    for digit in DIGITS:
        yield digit

    yield '22'
    yield '23'
    yield '333'
    yield '323'
    yield '7777'
    yield '7878'

    yield '2'*N
    
    for _ in range(5):
        for yes in [True, False]:
            n = N if yes else N-1

            s = [rand.choice(DIGITS)]
            while len(s) < n:
                d = rand.choice(DIGITS)
                if d != s[-1]:
                    s.append(d)
            
            if not yes:
                i = rand.randint(n//2 - n//5, n//2 + n//5)
                s.insert(i, s[i])
            
            yield ''.join(s)

if __name__ == '__main__':
    write_to_files(format_case, gen_random, *argv[1:])
