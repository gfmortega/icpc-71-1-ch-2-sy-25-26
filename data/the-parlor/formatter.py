"""Prints the test data in the correct input format."""

from kg.formatters import * ### @import

@formatter
def format_case(stream, cases, *, print, **kwargs):
    ... # write your formatter here

    # example:
    print(len(cases))
    for arr in cases:
        print(*arr, sep='\n')
        print('-'*75)
