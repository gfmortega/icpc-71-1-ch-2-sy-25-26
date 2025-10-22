def solve(s, offset):
    def count_duplicates(i, j):
        done = set()
        ans = 0
        for k in range(i, j):
            if s[k] in done:
                ans += 1
            done.add(s[k])
        return ans

    total = count_duplicates(0, offset)
    for i in range(offset, len(s), 7):
        total += count_duplicates(i, min(i+7, len(s)))
    return total

s = input()
print(min(
    solve(s, offset)
    for offset in range(min(10, len(s)))
))