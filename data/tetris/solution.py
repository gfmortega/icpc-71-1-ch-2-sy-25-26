def count_duplicates(bag):
    return len(bag) - len(set(bag))

def solve(s, offset):
    total = count_duplicates(s[:offset])
    for i in range(offset, len(s), 7):
        total += count_duplicates(s[i:i+7])
    return total

s = input()
print(min(
    solve(s, offset)
    for offset in range(min(7, len(s)))
))