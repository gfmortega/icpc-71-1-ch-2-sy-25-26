from sys import *
from kg.generators import * ### @import
from formatter import * ### @import

A = 10**18

@listify
def gen_random(rand, *args):
    N = int(args[0])

    for n in [N-1, N]:
        a = ''.join(str(i & 1) for i in range(n))
        b = ''.join(str((i+1) & 1) for i in range(n))
        yield a, b
        yield b, a

        c = '0'*n
        d = '1'*n
        yield c, d
        yield d, c

        for _ in range(3):
            x = ''.join(rand.choice(['0', '1']) for _ in range(n))
            y = ''.join(rand.choice(['0', '1']) for _ in range(n))
            yield x, y
            yield a, y
            yield x, b
            yield x, c
            yield d, y


if __name__ == '__main__':
    write_to_files(print_to_file, gen_random, *argv[1:])