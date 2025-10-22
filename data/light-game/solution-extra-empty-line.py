def get_nbhd(s, i):
    l = s[i-1]
    m = s[i]
    r = s[i+1] if i+1 < len(s) else s[0]
    return l + m + r

def get_press_count(pattern):
    if pattern in ['100', '011']:
        return 1
    elif pattern in ['000', '101', '010', '111']:
        return 2
    elif pattern in ['001', '110']:
        return 3
    else:
        raise RuntimeError('Impossible case')

s = list(input())
t = list(input())

moves = []
for i in range(len(s)):
    if s[i] != t[i]:
        moves.extend((i+1 for _ in range(get_press_count(get_nbhd(s, i)))))
        s[i] = t[i]

print('YES')
print(len(moves))
if len(moves) > 0:
    print(*moves)
