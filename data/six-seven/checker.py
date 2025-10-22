from kg.checkers import * ### @import
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from functools import wraps

class ParseError(RuntimeError):
    ...

class EvaluateError(RuntimeError):
    ...

class Evaluatable(ABC):
    @abstractmethod
    def evaluate(self) -> int:
        ...

class State(Enum):
    EXPECT_EXPRESSION = 0
    READING_NUMBER = 1
    NUMBER_ENDED = 2
    SUBEXP_ENDED = 3

LIM = 2**64

class Number(Evaluatable):
    value: int
    def __init__(self, x: int):
        self.value = x

    def add_digit(self, d: int):
        self.value = 10*self.value + d
        if self.value > LIM:
            return ParseError('Too-large number literal found')

    def evaluate(self):
        if self.value in [6, 7]:
            return self.value
        else:
            raise EvaluateError(f'Unallowed literal found: {self.value}')

@dataclass
class Operator:
    precedence: int
    combine: Callable[[int, int], int]

def safe(func: Callable[[int, int], int]):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ans = func(*args, **kwargs)
        if abs(ans) > LIM:
            raise EvaluateError(f'intermediate value of {ans} is too large')
        return ans
    return wrapper

@safe
def concat(x: int, y: int):
    return int(str(x) + str(y))

@safe
def sub(x: int, y: int):
    if x >= y:
        return x - y
    else:
        raise EvaluateError(f'Produced {x-y}')

@safe
def dupe(x: int, y: int):
    if y == 0:
        raise EvaluateError(f'cannot have {x}*0')
    if x != 0 and len(str(x)) * y > 20:
        raise EvaluateError(f'intermediate value of {x}*{y} is too large')
    else:
        return int(str(x) * y)

@safe
def div(x: int, y: int):
    if y == 0:
        raise EvaluateError('cannot divide by 0')
    if x % y != 0:
        raise EvaluateError('division produced non-integer')
    return x // y

OPS = {
    '+': Operator(0, concat),
    '-': Operator(0, sub),
    '*': Operator(1, dupe),
    '/': Operator(1, div),
}

class Expression(Evaluatable):
    children: list[Evaluatable]
    operators: list[Operator]

    def __init__(self):
        self.children = []
        self.operators = []

    def start_number(self, digit: str):
        self.children.append(Number(int(digit)))

    def add_digit(self, digit: str):
        if not self.children:
            raise RuntimeError('add_digit called on empty child')
        num: Number = self.children[-1]
        if not isinstance(self.children[-1], Number):
            raise RuntimeError('add_digit called w/ Number not most recent child')
        num.add_digit(int(digit))

    def add_operator(self, op: Operator):
        self.operators.append(op)

    def add_subexpression(self, child: 'Expression'):
        self.children.append(child)

    def evaluate(self):
        if len(self.children) == 0:
            raise RuntimeError('there are no children!')
        if len(self.children) != len(self.operators) + 1:
            raise RuntimeError('uneven children & operator count')

        OPERATOR_LB = min((op.precedence for op in self.operators), default=0)
        OPERATOR_UB = max((op.precedence for op in self.operators), default=-1)

        prev = [child.evaluate() for child in self.children]
        ops = list(self.operators)
        for v in reversed(range(OPERATOR_LB, OPERATOR_UB+1)):
            curr = [prev[0]]
            held_ops = []
            for x, op in zip(prev[1:], ops):
                if op.precedence == v:
                    curr[-1] = op.combine(curr[-1], x)
                else:
                    curr.append(x)
                    held_ops.append(op)
            prev = curr
            ops = held_ops

        if len(prev) != 1:
            raise RuntimeError(f'ended up with {len(prev)} children after eval, somehow')
        ans, = prev
        return ans

def process(line: str, i=0, is_root=True) -> tuple[Expression, int]:
    state = State.EXPECT_EXPRESSION
    expression = Expression()

    while i < len(line):
        c = line[i]
        if c == ' ':
            if state == State.READING_NUMBER:
                state = State.NUMBER_ENDED
        elif c == '(':
            if state == State.EXPECT_EXPRESSION:
                subexp, jump = process(line, i+1, False)
                expression.add_subexpression(subexp)
                i = jump
                state = State.SUBEXP_ENDED
            else:
                raise ParseError(f'Not expecting ( at character {i}')
        elif c == ')':
            if state in [State.READING_NUMBER, State.NUMBER_ENDED, State.SUBEXP_ENDED]:
                if is_root:
                    raise ParseError(f'Unmatched ) at character {i}')
                else:
                    return expression, i
            else:
                raise ParseError(f'Not expecting ) at character {i}')
            
        elif c.isdigit():
            if state == State.EXPECT_EXPRESSION:
                expression.start_number(c)
                state = State.READING_NUMBER
            elif state == State.READING_NUMBER:
                expression.add_digit(c)
            elif state in [State.NUMBER_ENDED, State.SUBEXP_ENDED]:
                raise ParseError(f'Not expecting a digit at this time')
            else:
                raise RuntimeError('Impossible case')

        elif c in OPS:
            if state == State.EXPECT_EXPRESSION:
                raise ParseError(f'expecting an expression, got {c} instead')
            elif state in [State.READING_NUMBER, State.NUMBER_ENDED, State.SUBEXP_ENDED]:
                expression.add_operator(OPS[c])
                state = State.EXPECT_EXPRESSION
            else:
                raise RuntimeError('Impossible case')

        else:
            raise ParseError(f'{c} is not an accepted character')
        
        i += 1

    # should have returned from nested expression due to ) not hit the end...
    if not is_root:
        raise ParseError(f'Unbalanced parentheses')

    if state == State.EXPECT_EXPRESSION:
        raise ParseError(f'line ended unexpectedly, expected another expression')

    return expression, i
            
def evaluate(line: str):
    if len(line) > 1000:
        raise ParseError('expression is too long!')
    else:
        expression, i = process(line)
        return expression.evaluate()


def get_int(file,exc=Exception):
    try:
        return int(next(file).rstrip())
    except Exception as e:
        raise exc("could not read ")

def get_line(file,exc=Exception):
    try:
        return next(file).rstrip()
    except Exception as e:
        raise exc("could not read line properly") from e
    

@set_checker(no_extra_chars=['input', 'output'])
def check_solution(input_file, output_file, judge_file, **kwargs):
    n = get_int(input_file, exc=WA)
    line = get_line(output_file, exc=WA)

    try:
        ans = evaluate(line)
        if ans == n:
            return 1.0
        else:
            raise WA(f'{ans} != desired {n}')
    except (ParseError, EvaluateError) as e:
        raise WA(str(e))
    
    


if __name__ == '__main__': chk(title="Silverbach's Conjecture")
