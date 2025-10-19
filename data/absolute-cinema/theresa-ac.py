# Theresa's attempt
n, r = [int(x) for x in input().split()]
a = [int(x) for x in input().split()]

s = sorted(a)
span = [x for x in s if x <= r]

if len(span) == 0: # edit: forgot na span can be empty, area is a trapezoid
    print(
        ((s[0]-r) + s[0]) * r // 2 # (b1+b2)*h/2
    )
else:
    # area of leftmost triangle
    first_triangle = span[0]*span[0] // 2

    # sum of area of intermediate triangles
    int_area = 0
    for tri in range(1,len(span)):
        dist = span[tri] - span[tri-1]
        int_area += dist*dist // 4

    # area of rightmost triangle (or shape)
    if len(s) == len(span) or r*2 < s[len(span)-1]+s[len(span)]: # rightmost shape is a triangle
        dist = r-span[-1]
        last_shape = dist*dist // 2
    else: # some weird shape
        base_bigger = s[len(span)]-span[-1]
        bigger_triangle = base_bigger*base_bigger // 4
        base_smaller = s[len(span)]-r
        smaller_triangle = base_smaller*base_smaller // 2
        last_shape = bigger_triangle-smaller_triangle

    print(first_triangle+int_area+last_shape)