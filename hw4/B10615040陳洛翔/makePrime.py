#coding=utf-8 
import random
from random import randint

# make random binary number which its MSB and LSB are '1'
def makeRandomNum(bits):  
    list = []
    list.append('1')
    for i in range(bits - 2):
        c = random.choice(['0', '1'])
        list.append(c)
    list.append('1')
    res = int(''.join(list),2)
    return res

# square and multiply, 
# x^n mod P = (x*x)^(n/2) mod P = ((x*x) mod P) ^ (n/2) mod P
def bigMod(x, n, p): 
    if n == 0:
        return 1
    res = bigMod((x * x) % p, n >> 1, p)
    if n & 1 != 0:
        res = (res * (x)) % p 
    return res

# Miller Rabin Test
def MillerRabin(a, p):
    if bigMod(a, p - 1, p) == 1:
        u = (p-1) >> 1
        while (u & 1) == 0:
            t = bigMod(a, u, p)
            if t == 1:
                u = u >> 1
            else:
                if t == p - 1:
                    return True
                else:
                    return False
        else:
            t = bigMod(a, u, p)
            if t == 1 or t == p - 1:
                return True
            else:
                return False
    else:
        return False

# Miller Rabin Test for k times
def MillerRabinTest(p, k): 
    while k > 0:
        a = randint(2, p - 1)
        if not MillerRabin(a, p):
            return False
        k = k - 1
    return True

# make n bits prime number 
def makePrime(bits):
    while 1:
        # make n bits number
        d = makeRandomNum(bits)
        for i in range(50):
            # Miller Rabin Test d + 2*(i) for 5 times
            u = MillerRabinTest(d+2*(i), 5)
            if u:
                # i get it
                b = d + 2*(i)
                break
            else:
                continue
        if u:
            return b
        else:
            continue