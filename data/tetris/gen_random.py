"""Generates random tests."""

from sys import *
from kg.generators import * ### @import
from formatter import * ### @import
from itertools import chain

@listify
def gen_random(rand, *args):
    # example:
    N, = map(int,args[:1])

    letters = 'IJLOSTZ'
    for c in letters:
        yield c
        yield c*2
        yield c*3
        yield c*N

    for i in range(7):
        s = []
        while len(s) + 7 <= N-i:
            s.extend(rand.shuffled(letters))
        s = rand.shuffled(letters)[:i] + s
        s.extend(rand.shuffled(letters)[:N-len(s)])
        yield ''.join(s)

        for _ in range(int(N**0.5)):
            i = rand.randint(0, N-1)
            s[i] = rand.choice(letters)
        yield ''.join(s)

    for _ in range(10):
        yield ''.join(rand.choice(letters) for _ in range(N))


if __name__ == '__main__':
    write_to_files(format_case, gen_random, *argv[1:])
