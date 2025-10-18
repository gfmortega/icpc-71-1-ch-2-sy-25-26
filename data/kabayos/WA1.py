n, c, k = [int(x) for x in input().split()]
a = [int(x) for x in input().split()]

a.sort(reverse=True)
a[-1] = min(c, a[-1] + k)

print(sum(x**2 for x in a))
