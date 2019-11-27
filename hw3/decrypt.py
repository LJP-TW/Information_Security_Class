import numpy as np
from PIL import Image
from Crypto.Cipher import AES
import sys

# get parameters
mode = sys.argv[1]
key = sys.argv[2]
path = sys.argv[3]

# save to temp bmp image
p = Image.open(path)
p.save('dec.bmp')

ciphertext = ''

with open("dec.bmp", "rb") as f:
    f = f.read()
    
    # Get Image Information (Without Header)
    trimmed = f[64:-2]

    # Padding
    paddingNum = 16 - (len(trimmed)%16)
    if paddingNum > 0:
        trimmed = trimmed + '0' * paddingNum
    
    # ECB
    if mode == 'ECB':
        cipher = AES.new(key, AES.MODE_ECB)
        ciphertext = ''.join([cipher.decrypt(trimmed[index: index+16]) for index in range(0, len(trimmed), 16)])
    
    # CBC
    else:
        IV = '0000111122223333'
        for index in range(16, len(trimmed), 16):
            cipher = AES.new(key, AES.MODE_CBC, trimmed[index-16: index])
            ciphertext = ciphertext + cipher.decrypt(trimmed[index: index+16])
            
        
        cipher = AES.new(key, AES.MODE_CBC, IV)
        ciphertext = cipher.decrypt(trimmed[0:16]) + ciphertext

    ciphertext = ciphertext[:len(ciphertext)-paddingNum]
    ciphertext = f[0:64] + ciphertext + f[-2:]


# Write it to bmp file
with open("dec.bmp", "w") as f:
    f.write(ciphertext)


print('finish')