def f(x):
    return x**2 - 3

def solve(s, t):
    if s in [-2, -1, 1, 2]:
        if s >= t:
            return 0
        elif f(s) >= t:
            return 1
        elif f(f(s)) >= t:
            return 2
        else:
            return 'MOVE ON'

    seeds = 0
    while not (s >= t):
        s = f(s)
        seeds += 1
    return seeds

s, t = [int(x) for x in input().split()]
print(solve(s, t))
