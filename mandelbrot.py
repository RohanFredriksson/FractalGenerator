import cmath

def compute(a,b,iterations):

    c = complex(a,b)
    z = complex(0,0)
    k = 0

    while k < iterations:

        z = z**2 + c
        k = k + 1

        if abs(z) > 2:
            break

    if k < iterations:
        return k / iterations
    
    return 0