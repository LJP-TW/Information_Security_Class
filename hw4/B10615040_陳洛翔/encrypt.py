import sys
sys.setrecursionlimit(1000000)
from makePrime import bigMod

# get plaintext
plaintext = sys.argv[1]
# add 100 to each ascii to ensure each characters occupy
# 3 bits in Number plaintext 
plaintext = int(''.join([str(ord(c)+100) for c in plaintext]))

# Read public key
with open('publicKey.txt', 'r') as f:
    L = f.readlines()
    N = int(L[0].strip())
    E = int(L[1].strip())

# encrypt
cipherText = bigMod(plaintext, E, N)

# write ciphertext to text file 
with open('ciphertext.txt', 'w') as f:
    f.write(str(cipherText))

