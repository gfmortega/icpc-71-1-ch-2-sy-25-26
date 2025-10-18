from sys import *
from kg.validators import * ### @import

bounds = {
    'n': 3 <= +Var <= 100,
    'B': set('01'),
}


@validator(bounds=bounds)
def validate_file(file, *, lim):
    [s] = file.read.token(charset=lim.B).eoln
    [t] = file.read.token(charset=lim.B).eoln.eof
    ensure(len(s) in lim.n and len(t) in lim.n and len(s) == len(t))

if __name__ == '__main__':
    validate_file(stdin)
