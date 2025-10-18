"""Prints the test data in the correct input format."""

from kg.formatters import * ### @import

@formatter
def format_case(stream, cases, *, print, **kwargs):
    ... # write your formatter here

    a, c, k = cases
    print(len(a), c, k)
    print(*a)

