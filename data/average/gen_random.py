"""Generates random tests."""

from sys import *
from kg.generators import * ### @import
from formatter import * ### @import
from itertools import chain

@listify
def gen_random(rand, *args):
    def random_grade():
        mode = rand.randint(1, 100)
        if mode <= 30:
            return rand.randint(92, 100)
        elif mode <= 45:
            return rand.randint(87, 91)
        elif mode <= 60:
            return rand.randint(83, 86)
        elif mode <= 65:
            return rand.randint(78, 82)
        elif mode <= 75:
            return rand.randint(70, 77)
        elif mode <= 95:
            return rand.randint(60, 69)
        elif mode <= 99:
            return rand.randint(1, 59)
        else:
            return 0

    # example:
    N, A, = map(int,args[:2])
    yield [A, 0], 1
    yield [A for _ in range(N)], 1
    yield [A for _ in range(N)], N-1
    yield [0 for _ in range(N)], 1
    yield [0 for _ in range(N)], N-1

    for breakpoint in [92, 87, 83, 78, 70, 60]:
        a = []
        for _ in range((N-1)//2):
            k = rand.randint(1, 8)
            a.append(breakpoint - k)
            a.append(breakpoint + k)
        yield rand.shuffled(a), len(a)//2
        yield rand.shuffled(a) + [1], 1
        a[-1] -= 1
        yield rand.shuffled(a), len(a)//2
        yield rand.shuffled(a) + [1], 1

    for n in [N-1, N]:
        for k in [rand.randint(1, n-1), 1, 2, n//2, int(n**0.5), n-2, n-1]:
            yield [rand.randint(0, 100) for _ in range(n)], k
            for _ in range(5):
                yield [random_grade() for _ in range(n)], k


if __name__ == '__main__':
    write_to_files(format_case, gen_random, *argv[1:])
