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
ciphertext = 'CIPHERTEXT'

def padding(text):
    return text + [0 for i in range((16 - (len(text) % 16)))]

if mode == 'ECB':
    for w in range(width):
        for h in range(height):
            e = ''.join(chr(x) for x in padding(list(pixels[w, h])))
            c = [ord(x) for x in cipher.encrypt(e)]
            pixels[w, h] = tuple(c[:3])
            ciphertext += ''.join(chr(x) for x in c)
elif mode == 'CBC':
    IV = [ord(x) for x in list('0000111122223333')]
    for w in range(width):
        for h in range(height):
            e = ''.join(chr(x^y) for x, y in zip(padding(list(pixels[w, h])), IV))
            c = [ord(x) for x in cipher.encrypt(e)]
            pixels[w, h] = tuple(c[:3])
            ciphertext += ''.join(chr(x) for x in c)
            IV = c
else:
    print('Non-supported mode')
    exit()

inputImage.save(outpath)
with open(outpath, 'a') as f:
    f.write(ciphertext)

