from sys import *
from kg.validators import * ### @import

bounds = {
    'n': 1 <= +Var <= 10**12,
}


@validator(bounds=bounds)
def validate_file(file, *, lim):
    [n] = file.read.int(lim.n).eoln.eof

if __name__ == '__main__':
    validate_file(stdin)
