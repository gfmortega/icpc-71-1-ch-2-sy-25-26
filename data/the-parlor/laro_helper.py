from itertools import product
def printy(s):
    print(f"    '{s}',")


exist = ['are', 'are not']
colors = ['blue', 'white', 'black']
bools = ['true', 'false']

for are, color in product(exist, colors):
    printy(f'The gems {are} in the {color} box.')

for color, bool in product(colors, bools):
    printy(f'The statement on the {color} box is {bool}.')

for bool in bools:
    printy(f'The statement on the box with the gems is {bool}.')

for bool in bools:
    printy(f'The statements on the empty boxes are both {bool}.')

for bool in bools:
    printy(f'Exactly one box has a statement that is {bool}.')

for bool in bools:
    printy(f'Exactly two boxes have a statement that is {bool}.')