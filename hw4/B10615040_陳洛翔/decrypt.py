import sys
sys.setrecursionlimit(1000000)
from makePrime import bigMod


# read cipher text
with open('ciphertext.txt', 'r') as f:
    L = f.readlines()
    ciphertext = int(L[0].strip())

# read private Key
with open('privateKey.txt', 'r') as f:
    L = f.readlines()
    N = int(L[0].strip())
    D = int(L[1].strip())

# get plaintext number
plaintext = str(bigMod(ciphertext, D, N))

# subtract 100 to each ascii cuz we added 100 before
# and print our plaintext.
print(''.join([chr(int(plaintext[i:i+3])-100) 
    for i in range(0, len(plaintext), 3)]))

