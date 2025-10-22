n, c, k = [int(x) for x in input().split()]
a = [int(x) for x in input().split()]

ans = 0
a.sort()
for x in reversed(a):
    while x < c and k > 0:
        x += 1
        k -= 1
    ans += x**2

print(ans)
