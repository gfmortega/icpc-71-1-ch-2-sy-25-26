n, c, k = [int(x) for x in input().split()]
a = [int(x) for x in input().split()]

print(sum(c**2 for x in a))
