import sys
sys.setrecursionlimit(1000000)
from makePrime import bigMod



with open('ciphertext.txt', 'r') as f:
    L = f.readlines()
    ciphertext = int(L[0].strip())


with open('privateKey.txt', 'r') as f:
    L = f.readlines()
    N = int(L[0].strip())
    D = int(L[1].strip())

plaintext = str(bigMod(ciphertext, D, N))

print(''.join([chr(int(plaintext[i:i+3])-100) 
    for i in range(0, len(plaintext), 3)]))

