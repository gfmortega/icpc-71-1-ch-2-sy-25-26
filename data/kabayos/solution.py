n, c, k = [int(x) for x in input().split()]
a = [int(x) for x in input().split()]

a.sort(reverse=True)
for i in range(n):
    inc = min(c - a[i], k)
    a[i] += inc
    k -= inc

print(sum(x**2 for x in a))
