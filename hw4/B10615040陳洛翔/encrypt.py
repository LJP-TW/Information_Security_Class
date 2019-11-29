import sys
sys.setrecursionlimit(1000000)
from makePrime import bigMod


plaintext = sys.argv[1]
plaintext = int(''.join([str(ord(c)+100) for c in plaintext]))

with open('publicKey.txt', 'r') as f:
    L = f.readlines()
    N = int(L[0].strip())
    E = int(L[1].strip())


cipherText = bigMod(plaintext, E, N)

with open('ciphertext.txt', 'w') as f:
    f.write(str(cipherText))

