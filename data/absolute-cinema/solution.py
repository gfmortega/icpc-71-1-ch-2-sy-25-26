def half_tri(b):
    return b**2 // 2

def step_tri(b):
    return b**2 // 4

def solve(a, R):
    a = sorted(set(a))

    # if chopped off immediately, return only the chopped-off left boundary
    if R < a[0]:
        return half_tri(a[0]) - half_tri(a[0] - R)

    # WLOG, a[0] <= R
    # add the left boundary first
    total = a[0]**2 // 2
    for i in range(1, len(a)):
        l, r = a[i-1], a[i]
        m = (l + r)//2
        
        if R < l:
            break
        elif R <= m:
            total += half_tri(R - l)
        elif R <= r:
            total += step_tri(r - l) - half_tri(r - R)
        else:
            total += step_tri(r - l)

        
    
    # add also the right boundary, if it exists
    if a[-1] < R:
        total += half_tri(R - a[-1])

    return total

n, R = [int(x) for x in input().split()]
a = [int(x) for x in input().split()]
print(solve(a, R))
