from makePrime import makePrime, bigMod
from gcd import gcd, ext_gcd
import sys
sys.setrecursionlimit(1000000)

# initial d = -1
d = -1

# do until d is > 0
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

# write publicKey(n,e) to text file
with open('./publicKey.txt', 'wb') as f:
    f.write(str(n))
    f.write('\n')
    f.write(str(e))

# write privateKey(n,d) to text file
with open('./privateKey.txt', 'wb') as f:
    f.write(str(n))
    f.write('\n')
    f.write(str(d))

print('finish')



