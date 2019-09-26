#!/usr/bin/python3

import sys

key = sys.argv[2]
p = sys.argv[3]

if sys.argv[1] == 'caesar':
    c = ''.join(chr((ord(x) - ord('a') + int(key)) % 26 + ord('a')) for x in p).upper()
    print(c)


