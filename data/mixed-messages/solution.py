def decode(c):
    return "**adgjmptw"[int(c)]

s = input()
if all(s[i] != s[i+1] for i in range(len(s) - 1)):
    print('CLEAR')
    print(''.join(decode(c) for c in s))
else:
    print('AMBIGUOUS')
