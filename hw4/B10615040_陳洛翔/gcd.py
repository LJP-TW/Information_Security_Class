
# normal gcd
def gcd(a,b):
    if(b == 0):
        return a
    return gcd(b, a%b)

# extended gcd
def ext_gcd(a,b):
    if(b == 0):
        return a, 1, 0

    r, x1, y1 = ext_gcd(b, a%b)
    x = y1
    y = x1 - a // b * y1

    return r, x, y




