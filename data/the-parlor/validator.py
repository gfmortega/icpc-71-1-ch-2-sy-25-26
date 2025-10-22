"""Checks whether the input file is valid."""

from sys import *
from kg.validators import * ### @import

bounds = {
    'T': 1 <= +Var <= 400,
}

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

@validator(bounds=bounds)
def validate(stream, *, lim):
    ... # write your validator here

    # example:
    [T] = stream.read.int(lim.T).eoln
    for cas in range(T):
        [statement1, statement2, statement3, divider] = stream.read.line().eoln.line().eoln.line().eoln.line().eoln
        # print(statement1, statement2, statement3, divider)
        ensure(statement in statements for statement in [statement1, statement2, statement3])
        ensure(divider == '-'*75)
    [] = stream.read.eof

    # other possibilities
    # [x, y, z] = stream.read.real(lim.x).space.real(lim.y).space.int(lim.z).eoln
    # [line] = stream.read.line(lim.s).eoln
    # [name] = stream.read.token(lim.name).eoln


if __name__ == '__main__':
    validate(stdin)
