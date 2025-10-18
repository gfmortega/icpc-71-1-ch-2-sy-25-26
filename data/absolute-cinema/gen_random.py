"""Generates random tests."""

from sys import *
from kg.generators import * ### @import
from formatter import * ### @import
from itertools import chain

@listify
def gen_random(rand, *args):
    # example:
    N, A, = map(int,args[:2])
    for n in [N-1, N]:
        for mode in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            a = [2*rand.randint(2, A//2 - 1) for _ in range(n)]
            a_ = sorted(a)

            if mode == 1:
                R = a_[0] - 2
            elif mode == 2:
                R = a_[0]
            elif 3 <= mode <= 7:
                first = True
                while first or r - l <= 8:
                    first = False
                    i = rand.randint(n//2 - n//4, n//2 + n//4)
                    l = a_[i-1]
                    r = a_[i]
                    m = (l + r) // 2

                if mode == 3:
                    R = l
                elif mode == 4:
                    R = 2*rand.randint(l//2 + 1, m//2 - 1)
                elif mode == 5:
                    R = 2*((m-1)//2)
                elif mode == 6:
                    R = 2*((m+1)//2)
                elif mode == 7:
                    R = 2*rand.randint(m//2 + 1, r//2 - 1)
                else:
                    raise RuntimeError(f'{mode} is invalid')

            elif mode == 8:
                R = a[-1]
            
            elif mode == 9:
                R = 2*rand.randint(a[-1]//2, A//2)

            elif mode == 10:
                R = 2*rand.randint(1, A//2)

            yield a, R



    yield list(reversed(list(2*i for i in range(1, n+1)))), 2*(n//4)
    yield [2*(A//4) for _ in range(n)], 2
    yield [2*(A//4) for _ in range(n)], 2*(A//4)
    yield [2*(A//4) for _ in range(n)], 2*(A//2)

if __name__ == '__main__':
    write_to_files(format_case, gen_random, *argv[1:])
