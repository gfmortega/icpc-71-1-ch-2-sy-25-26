def f(x):
    return x**2 - 3

def solve(s, t):
    for i in range(10):
        if s >= t:
            return i
        else:
            s = f(s)
    return 'MOVE ON'

s, t = [int(x) for x in input().split()]
print(solve(s, t))
