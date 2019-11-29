from makePrime import makePrime, bigMod
from gcd import gcd, ext_gcd
# import time

import sys
sys.setrecursionlimit(1000000)

d = -1

while (d < 0):
    print('find p')
    p = makePrime(1024)

    print('find q')
    q = makePrime(1024)
    n = p * q
    r = (p-1) * (q-1)

    print('find d')
    e = 65537

    a, d, b = ext_gcd(e, r)

with open('./publicKey.txt', 'wb') as f:
    f.write(str(n))
    f.write('\n')
    f.write(str(e))


with open('./privateKey.txt', 'wb') as f:
    f.write(str(n))
    f.write('\n')
    f.write(str(d))

print('finish')



