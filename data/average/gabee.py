grades = ["F", "D", "C", "C+", "B", "B+", "A"]
breakpts = [0, 60, 70, 78, 83, 87, 92]

def get_grade(s, n):    
    return grades[len(list(filter(lambda x: s >= x * n, breakpts))) - 1]

n, k = map(int, input().split(" "))

s = list(map(int, input().split(" ")))

print(get_grade(sum(s), n))
print(get_grade(sum(sorted(s)[k:]), n - k))