n = int(input())
a = [int(x) for x in input().split()]
c = [int(x) for x in input().split()]
for i in range(n):
    a[i] -= 1
    c[i] -= 1

c_inv = [None for _ in range(n)]
for i in range(n):
    c_inv[c[i]] = i

b = [None for _ in range(n)]
for i in range(n):
    b[a[i]] = c_inv[i]

for i in range(n):
    b[i] += 1
print(*b)