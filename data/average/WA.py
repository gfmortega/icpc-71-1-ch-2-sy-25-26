def numerical_grade_to_letter_grade(x: float) -> str:
    if 92 < x:
        return 'A'
    elif 87 < x:
        return 'B+'
    elif 83 < x:
        return 'B'
    elif 78 < x:
        return 'C+'
    elif 70 < x:
        return 'C'
    elif 60 < x:
        return 'D'
    else:
        return 'F'
    
def average(a: list[int]) -> float:
    return sum(a)/len(a)

n, k = [int(x) for x in input().split()]
a = [int(x) for x in input().split()]

print(numerical_grade_to_letter_grade(average(a)))
print(numerical_grade_to_letter_grade(average(sorted(a)[k:])))