"""Generates random tests."""

from sys import *
from kg.generators import * ### @import
from formatter import * ### @import
from itertools import chain

@listify
def gen_random(rand, *args):
    # example:
    N, C, K = map(int,args[:3])
    for _ in range(5):
        c = rand.randint(C//2, C)
        k = rand.randint(K-10, K)
        yield [rand.randint(1, c) for _ in range(N)], c, k
    for _ in range(5):
        c = rand.randint(C//2, C)
        k = rand.randint(K-10, K)
        yield [c - rand.randint(1, K//(c+2)) for _ in range(N)], c, k
    for _ in range(5):
        c = rand.randint(C//2, C)
        k = rand.randint(K-10, K)
        yield [c - rand.randint(1, K//(c//2+2)) for _ in range(N//2)] + [rand.randint(1, K//(c//2+2)) for _ in range(N//2)], c, k



if __name__ == '__main__':
    write_to_files(format_case, gen_random, *argv[1:])
