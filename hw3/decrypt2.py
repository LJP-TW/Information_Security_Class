#!/usr/bin/python
import numpy as np
from PIL import Image
from Crypto.Cipher import AES
import sys

# get parameters
mode = sys.argv[1]
key = sys.argv[2]
inpath = sys.argv[3]
outpath = sys.argv[4]

inputImage = Image.open(inpath)
width, height = inputImage.size
pixels = inputImage.load()
cipher = AES.new(key, AES.MODE_ECB)

with open(inpath, 'r') as f:
    binary = f.read()
    idx = binary.find('CIPHERTEXT') + len('CIPHERTEXT')

    if mode == 'ECB':
        for w in range(width):
            for h in range(height):
                c = binary[idx:idx+16]
                e = [ord(x) for x in cipher.decrypt(c)]
                pixels[w, h] = tuple(e[:3])
                idx += 16
    elif mode == 'CBC':
        IV = list('0000111122223333')
        for w in range(width):
            for h in range(height):
                c = binary[idx:idx+16]
                e = [ord(x) ^ ord(y) for x, y in zip(cipher.decrypt(c), IV)]
                pixels[w, h] = tuple(e[:3])
                idx += 16
                IV = c
    elif mode == 'OFB':
        IV = '0000111122223333'
        for w in range(width):
            for h in range(height):
                k = cipher.encrypt(IV)
                c = binary[idx:idx+16]
                e = [ord(x) ^ ord(y) for x, y in zip(c, k)]
                pixels[w, h] = tuple(e[:3])
                idx += 16
                IV = k
    else:
        print('Non-supported mode')
        exit()
    
    inputImage.save(outpath)


