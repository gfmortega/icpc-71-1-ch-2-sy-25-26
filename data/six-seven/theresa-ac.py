# Theresa's attempt

# ways to construct each digit
digits = [
    '(6 - 6)', # 0 (7 char)
    '(7 - 6)', # 1 (7 char)
    '(7 - (6 - (7-6)))', # 2 (17 char)
    '(((6+7 - 7) / 6) - 7)', # 3 (21 char)
    '(((6+7 - 7) / 6) - 6)', # 4 (21 char)
    '(6 - (7-6))', # 5 (11 char)
    '6', # 6 (1 char)
    '7', # 7 (1 char)
    '(((6 - (7-6)) + 6) / 7)', # 8 (23 char)
    '((6+7 - 6 - 7) / 6)' # 9 (19 char)
]

# input is at most 11 digits, so max string is 88_888_888_888 
# max length of expression (assuming sep = ' + ') is 23*11 + 3*10 = 283 < 1000 (computer wont explode yay)

# input
n = [int(x) for x in [*input()]] # instead of parsing to int, let's parse it to a list of digits

# take corresponding expressions per digit
expressions = [digits[i] for i in n]

# output: add them all together
print(*expressions, sep=' + ')