"""Generates random tests."""

from sys import *
from kg.generators import * ### @import
from formatter import * ### @import
from itertools import product

statements = [
    'The gems are in the blue box.',
    'The gems are in the white box.',
    'The gems are in the black box.',
    'The gems are not in the blue box.',
    'The gems are not in the white box.',
    'The gems are not in the black box.',
    'The statement on the blue box is true.',
    'The statement on the blue box is false.',
    'The statement on the white box is true.',
    'The statement on the white box is false.',
    'The statement on the black box is true.',
    'The statement on the black box is false.',
    'The statement on the box with the gems is true.',
    'The statement on the box with the gems is false.',
    'The statements on the empty boxes are both true.',
    'The statements on the empty boxes are both false.',
    'Exactly one box has a statement that is true.',
    'Exactly one box has a statement that is false.',
    'Exactly two boxes have a statement that is true.',
    'Exactly two boxes have a statement that is false.',
]

@listify
def gen_random(rand, *args):
    ... # write your generator here
    T = 400
    ALL = iter(product(statements, repeat=3))
    for _ in range(0, len(statements)**3, T):
        yield [next(ALL) for _ in range(T)]


if __name__ == '__main__':
    write_to_files(format_case, gen_random, *argv[1:])
