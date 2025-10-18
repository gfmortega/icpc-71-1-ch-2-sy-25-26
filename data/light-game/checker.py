from kg.checkers import * ### @import
from collections import defaultdict


def get_integers(file, n, exc=Exception):
    try:
        a = list(map(int, next(file).rstrip().split()))
        if len(a) != n:
            raise exc("not {n} integers")
        return a
    except Exception as e:
        raise exc(f"could not read {n} integers")

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
    

@set_checker(no_extra_chars=['input'])
def check_solution(input_file, output_file, judge_file, **kwargs):
    s = list(map(int, get_line(input_file, exc=Fail)))
    t = get_line(input_file, exc=Fail)

    judge_verdict = get_line(judge_file, exc=Fail)
    output_verdict = get_line(output_file, exc=WA)

    if judge_verdict != output_verdict:
        raise WA('does not match verdict of judge')
    
    if output_verdict == judge_verdict == 'NO':
        return 1.0
    
    m = get_int(output_file, exc=WA)
    if not (0 <= m <= 3*10**5):
        raise WA(f'{m} invalid')
    
    if m > 0:
        moves = get_integers(output_file, m, exc=WA)
    else:
        moves = []

    for i in moves:
        i -= 1

        l = i-1
        if l == -1:
            l = len(s)-1
        r = i+1
        if r == len(s):
            r = 0

        if s[l] == 0 and s[r] == 0:
            s[l] = s[r] = 1
        elif s[l] == 1 and s[r] == 1:
            s[l] = s[r] = 0
            s[i] ^= 1
        elif s[l] == s[i] and s[i] != s[r]:
            s[l] ^= 1
            s[r] ^= 1
        elif s[l] != s[i] and s[i] == s[r]:
            s[i] = s[l]
        else:
            raise Fail('unexpected case in light-pressing')
        
    s = ''.join(str(b) for b in s)
    if s == t:
        return 1.0
    else:
        return WA(f'{s} != {t}')


if __name__ == '__main__': chk(title="Silverbach's Conjecture")
