from sys import *
from kg.generators import * ### @import
from formatter import * ### @import

A = 10**18

@listify
def gen_random(rand, *args):
    e = int(args[0])

    for d in range(1, 9+1):
        yield d
        yield int(str(d)*e)

    yield 10
    yield 10**e

    yield 1234567890
    yield 9876543210

    for _ in range(15):
        yield rand.randint(10**e //2, 10**e)

if __name__ == '__main__':
    write_to_files(print_to_file, gen_random, *argv[1:])