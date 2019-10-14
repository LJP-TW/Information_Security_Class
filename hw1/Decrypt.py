#!/usr/bin/python3
import sys
import string
import numpy as np

# Change all the stuff to lower_case
method = sys.argv[1].lower()
key = sys.argv[2].lower()
text = sys.argv[3].lower()

DEBUG = 0

if method == 'caesar':
    # Convert Key to Integer
    key = int(key)
    
    # Base ascii code for 'a'
    a = ord('a')
    
    # Decrypt each characters.
    print(''.join(chr(ord(c) - key) if(ord(c) - key >= a) else (chr(ord(c) - key + 26)) for c in text))

elif method == 'playfair':
    # Get a-z list
    mask = list(string.ascii_lowercase)
    
    # Remove 'j'
    mask.remove('j')

    # Generate 5*5 Key Table
    for c in key:
        mask.remove(c) 
    mask = np.array(list(key) + mask)
    mask = mask.reshape(5,5)
    
    # Decrypt 
    ans = ''
    for i in range(0, len(text), 2):
        # Get the two characters and each positions
        c1, c2 = text[i], text[i+1]
        y1, x1 = np.where(mask == c1)[0][0], np.where(mask == c1)[1][0]
        y2, x2 = np.where(mask == c2)[0][0], np.where(mask == c2)[1][0]

        # Decrypt it base on their positions correlation
        if(x1 == x2):
            ans += mask[(y1-1) if (y1-1) >= 0 else (y1 + 4)][x1]
            ans += mask[(y2-1) if (y2-1) >= 0 else (y2 + 4)][x1]
        elif(y1 == y2):
            ans += mask[y1][(x1-1) if (x1-1) >= 0 else (x1 + 4)]
            ans += mask[y1][(x2-1) if (x2-1) >= 0 else (x2 + 4)]
        else:
            ans += mask[y1][x2]
            ans += mask[y2][x1]

    print(ans)

elif method == 'vernam':
    lenKey = len(key)
    a = ord('a')
    ans = ''
    for i in range(len(text)):
        # Decrypt it by key
        ans += chr(((ord(text[i]) - a) ^ (ord(key[i % lenKey]) - a)) + a)

        # If it is decrypt by last charater of key, get the new key(plain text).
        if(i % len(key) == (len(key) - 1)):
            key = ans[i-lenKey+1 : i + 1]

    print(ans.lower())

elif method == 'row':

    # Conver plaintext to a table
    # To keep the dimension of each element in table, I fill the rest by '#' when the string is not longer enough.
    modKey = len(text) % len(key)
    divideKey = len(text) // len(key)

    # Generate a table base on modKey and divideKey
    table = np.full((len(key), len(text) // len(key) if modKey == 0 else len(text) // len(key) + 1), '')

    for i in range(1, len(key)+1):
        # Find which column I should insert my string.
        index = key.find(chr(ord('0') + i))

        # Get the string base on modkey and index.
        if(modKey == 0):
            table[index] = list(text[:divideKey])
            text = text[divideKey:]

        elif index >= modKey:
            table[index] = np.array(list(text[:divideKey]) + ['#'])
            text = text[divideKey:]
        else:
            table[index] = np.array(list(text[:divideKey + 1]))
            text = text[divideKey + 1:]
    
    #  Convert it to my answer and remove '#'
    ans = ''
    for i in range(divideKey + (modKey != 0)):
        ans += ''.join(list(table[:,i]))
    print(ans.replace('#', ''))
    
else:
    key = int(key)

    # How many chars that every row holds
    charCounts = []

    textlen = len(text)
    textlen -= key

    # key is too big, and the encryption will do nothing
    # so decryption will also do nothing
    if textlen <= 0:
        print(text)
        exit()

    quotient = textlen // (key - 1)
    remainder = textlen % (key - 1)

    # setting charCounts
    charCounts.append(1 + quotient // 2 + quotient % 2)
    for i in range(key - 2):
        charCounts.append(1 + quotient)
    charCounts.append(1 + quotient // 2)

    if DEBUG:
        print(textlen)
        print(quotient)
        print(remainder)

    if quotient % 2:
        pos = 1
        for i in range(remainder):
            charCounts[pos] += 1
            pos += 1
    else:
        pos = key - 2
        for i in range(remainder):
            charCounts[pos] += 1
            pos -= 1
    if DEBUG:
        print(charCounts) 

    textrows = [' '  for i in range(len(charCounts))]
    pos = 0
    for i, v in enumerate(charCounts):
        textrows[i] += text[pos:pos + v]
        pos += v

    if DEBUG:
        print('text ros:')
        print(textrows)

    c = ''
    pos = 0 
    direction = 1
    while True:
        if len(textrows[pos]) == 1:
            break
        
        c += textrows[pos][1]
        textrows[pos] = textrows[pos][1:]
        
        pos += direction

        if pos == key - 1:
            direction = -1
        if pos == 0:
            direction = 1

    print(c)    
