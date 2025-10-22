from enum import Enum
from itertools import product


class Kind(Enum):
    KNIGHT = 'knight'
    KNAVE = 'knave'

    def say(self, other):
        return other if self.truthteller else other.opp()

    def opp(self):
        match self:
            case Kind.KNIGHT:
                return Kind.KNAVE
            case Kind.KNAVE:
                return Kind.KNIGHT

    @property
    def truthteller(self):
        match self:
            case Kind.KNIGHT:
                return True
            case Kind.KNAVE:
                return False


class Statement(Enum):
    HAS_KNIGHT = "There is a knight among us."
    HAS_KNAVE = "There is a knave among us."
    MORE_KNIGHTS_THAN_KNAVES = "There are more knights than knaves."
    MORE_KNAVES_THAN_KNIGHTS = "There are more knaves than knights."
    ALL_SAME = "All of us are the same."
    OTHERS_SAME_DIFF_FROM_ME = "Those other two are the same, and different from me."
    OTHERS_DIFF = "I am different from one of those two, but the same as the other one."
    OTHERS_SAY_KNIGHT = "Both of those two would say I am a knight."
    OTHERS_SAY_KNAVE = "Both of those two would say I am a knave."
    OTHERS_SAY_DIFF = "If asked what I am, those two would give different answers."

    def consistent(self, *ks):
        self_k, *other_ks = ks
        return self.truth(*ks) == self_k.truthteller

    def truth(self, *ks):
        assert len(ks) == 3
        self_k, *other_ks = ks
        match self:
            case Statement.HAS_KNIGHT:
                return Kind.KNIGHT in ks
            case Statement.HAS_KNAVE:
                return Kind.KNAVE in ks
            case Statement.MORE_KNIGHTS_THAN_KNAVES:
                return ks.count(Kind.KNIGHT) > ks.count(Kind.KNAVE)
            case Statement.MORE_KNAVES_THAN_KNIGHTS:
                return ks.count(Kind.KNAVE) > ks.count(Kind.KNIGHT)
            case Statement.ALL_SAME:
                return len(set(ks)) == 1
            case Statement.OTHERS_SAME_DIFF_FROM_ME:
                return self_k not in other_ks and len(set(other_ks)) == 1
            case Statement.OTHERS_DIFF:
                return len(set(other_ks)) > 1
            case Statement.OTHERS_SAY_KNIGHT:
                return all(k.say(self_k) == Kind.KNIGHT for k in other_ks)
            case Statement.OTHERS_SAY_KNAVE:
                return all(k.say(self_k) == Kind.KNAVE for k in other_ks)
            case Statement.OTHERS_SAY_DIFF:
                return len({k.say(self_k) for k in other_ks}) > 1


def consistent(statements, kinds):
    return all(statement.consistent(kinds[idx], *(kind for i, kind in enumerate(kinds) if i != idx)) for idx, statement in enumerate(statements))


NAMES = 'Alice', 'Bob', 'Cindy'

def solve(*statements):
    assert len(statements) == len(NAMES)
    oks = {name: set() for name in NAMES}
    for kinds in product(Kind, repeat=len(NAMES)):
        if consistent(statements, kinds):
            for name, kind in zip(NAMES, kinds, strict=True):
                oks[name].add(kind)

    return oks if all(oks.values()) else None

UNCERTAIN = 'uncertain'
BAD = 'narrator: liar!'

def output_line(name, label):
    return f"{name}: {label}"

def label(ok):
    match [*ok]:
        case [s]:
            return s.value
        case _:
            return UNCERTAIN


def main():
    for _ in range(int(input())):
        if res := solve(*(Statement(input()) for _ in range(3))):
            for name in NAMES:
                print(output_line(name, label(res[name])))
        else:
            print(BAD)
        print('-'*15)
        input()


if __name__ == '__main__':
    main()
