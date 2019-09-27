#!/usr/bin/python3
import numpy as np
import sys

key = sys.argv[2].upper()
p = sys.argv[3].lower()

DEBUG = 0

if DEBUG:
    print(f'key : {key}')
    print(f'p   : {p}')

if sys.argv[1] == 'caesar':
    c = ''.join(chr((ord(x) - ord('a') + int(key)) % 26 + ord('a')) for x in p).upper()
    print(c)

elif sys.argv[1] == 'playfair':
    # Prepare table
    key = key.replace(' ', '')
    temp = ''
    for c in key:
        temp += c if c not in temp else ''
    temp += ''.join(x if x not in key else '' for x in 'ABCDEFGHIKLMNOPQRSTUVWXYZ')
    table = [temp[i:i+5] for i in range(0, 25, 5)]

    if DEBUG:
        print(f'table = {table}')

    # Initialize plaintext
    temp = p.replace(' ', '').upper().replace('J', 'I')
    p = ''
    i = 0
    while True:
        if i == len(temp):
            break
        elif i == len(temp) - 1:
            p += temp[i]
            p += 'X'
            break
        else:
            if temp[i] == temp[i + 1]:
                p += temp[i]
                p += 'X'
                i += 1
            else:
                p += temp[i]
                p += temp[i + 1]
                i += 2

    if DEBUG:
        print(f'p = {p}')

    # Find out cipher text
    cipher = ''
    for i in range(0, len(p), 2):
        x1, y1, x2, y2 = 0, 0, 0, 0
        for y, s in enumerate(table):
            if p[i] in s:
                y1 = y
                for x, c in enumerate(s):
                    if p[i] == c:
                        x1 = x
                        break
                break
        for y, s in enumerate(table):
            if p[i + 1] in s:
                y2 = y
                for x, c in enumerate(s):
                    if p[i + 1] == c:
                        x2 = x
                        break
                break
        if DEBUG:
            print(f'{p[i]}{p[i+1]} : {{{y1}, {x1}}}, {{{y2}, {x2}}}')

        if y1 == y2:
            # Both letters fall in the same row
            x1 = (x1 + 1) % 5
            x2 = (x2 + 1) % 5
        elif x1 == x2:
            # Both letters fall in the same column
            y1 = (y1 + 1) % 5
            y2 = (y2 + 1) % 5
        else:
            x1, x2 = x2, x1
        cipher += table[y1][x1]
        cipher += table[y2][x2]

        if DEBUG:
            print(f'{{{table[y1][x1]}{table[y2][x2]}}}')
    print(cipher)
    
elif sys.argv[1] == 'vernam':
    lenKey = len(key)
    lenP = len(p)
    A = ord('A')
    c = ''
    p = p.replace(' ', '').upper()

    if lenKey < lenP:
        key = key + p[:lenP - lenKey]
    
    for x, y in zip(p, key):
        c += chr(((ord(x) - A) ^ (ord(y) - A)) + A)

    if DEBUG:
        print(f'key : {key}')

    print(c)

elif sys.argv[1] == 'row':
    if len(p) % len(key) > 0:
        p += '#' * (len(key) - (len(p) % len(key)))
    
    p = np.array(list(p)).reshape(len(p) // len(key), len(key))
    ans = ''
    for i in range(1, len(key)+1):
        index = key.find(chr(ord('0')+i))
        ans += ''.join(p[:,index])
    print(ans.replace('#',''))

else:
    if len(p) % int(key) > 0:
        p += '#' * (int(key) - (len(p) % int(key)))

    t = np.array(list(p)).reshape(int(key), len(p) // int(key))

    if DEBUG:
        print(t)

    c = ''
    for i in range(len(p) // int(key)):
        c += ''.join(list(t[:,i]))

    c = c.replace('#', '')

    print(c)
