from itertools import product

colors = ['blue', 'white', 'black']
cInv = {
    color: i for i, color in enumerate(colors)
}
bInv = {
    'true': True,
    'false': False,
}
nInv = {
    'one': 1,
    'two': 2,
}

def parse_statement(line):
    tokens = line.split()
    if tokens[1] == 'gems':
        if tokens[3] == 'not':
            return lambda config, loc: loc != cInv[tokens[-2]]
        else:
            return lambda config, loc: loc == cInv[tokens[-2]]
    elif tokens[1] == 'statement':
        if tokens[4] in cInv:
            return lambda config, loc: config[cInv[tokens[4]]] is bInv[tokens[-1][:-1]]
        else:
            return lambda config, loc: config[loc] is bInv[tokens[-1][:-1]]
    elif tokens[1] == 'statements':
        return lambda config, loc: all(config[i] is bInv[tokens[-1][:-1]] for i in range(3) if i != loc)
    elif tokens[0] == 'Exactly':
        return lambda config, loc: sum(1 if config[i] is bInv[tokens[-1][:-1]] else 0 for i in range(3)) == nInv[tokens[1]]
    else:
        raise RuntimeError('Impossible case')

for _ in range(int(input())):
    statements = [parse_statement(input()) for _ in range(3)]
    input()

    possible = set()
    for config in product([True, False], repeat=3):
        if not (
            any(x is True for x in config) and
            any(x is False for x in config)
        ):
            continue
        for loc in range(3):
            if all(
                config[i] == statements[i](config, loc)
                for i in range(3)
            ):
                possible.add(loc)
    
    if len(possible) == 0:
        print('PARADOX')
    elif len(possible) == 1:
        loc, = possible
        print(colors[loc])
    else:
        print('AMBIGUOUS')
