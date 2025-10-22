def f(x):
    return x**2 - 3

def solve(s, t):
    seeds = 0
    done = []
    while not (s >= t):
        if s in done:
            return 'MOVE ON'
        else:
            done.append(s)

        s = f(s)
        seeds += 1
    return seeds

s, t = [int(x) for x in input().split()]
print(solve(s, t))
