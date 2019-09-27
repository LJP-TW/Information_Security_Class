import sys
import string
import numpy as np
method = sys.argv[1].lower()
key = sys.argv[2].lower()
text = sys.argv[3].lower()

if method == 'caesar':
    key = int(key)
    a = ord('a')
    print(''.join(chr(ord(c) - key) if(ord(c) - key >= a) else (chr(ord(c) - key + 26)) for c in text))

elif method == 'playfair':
    
    mask = list(string.ascii_lowercase)
    mask.remove('j')

    for c in key:
        mask.remove(c) 
    mask = np.array(list(key) + mask)
    mask = mask.reshape(5,5)
    
    ans = ''
    for i in range(0, len(text), 2):
        c1, c2 = text[i], text[i+1]
        y1, x1 = np.where(mask == c1)[0][0], np.where(mask == c1)[1][0]
        y2, x2 = np.where(mask == c2)[0][0], np.where(mask == c2)[1][0]

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
        ans += chr(((ord(text[i]) - a) ^ (ord(key[i % lenKey]) - a)) + a)
        if(i % len(key) == (len(key) - 1)):
            key = ans[i-lenKey+1 : i + 1]
    print(ans.lower())

elif method == 'row':

    modKey = len(text) % len(key)
    divideKey = len(text) // len(key)
    table = np.full((len(key), len(text) // len(key) if modKey == 0 else len(text) // len(key) + 1), '')

    for i in range(1, len(key)+1):
        index = key.find(chr(ord('0') + i))
        if(modKey == 0):
            table[index] = list(text[:divideKey])
            text = text[divideKey:]

        elif index >= modKey:
            table[index] = np.array(list(text[:divideKey]) + ['#'])
            text = text[divideKey:]
        else:
            table[index] = np.array(list(text[:divideKey + 1]))
            text = text[divideKey + 1:]
            
    ans = ''
    for i in range(divideKey + (modKey != 0)):
        ans += ''.join(list(table[:,i]))
    print(ans.replace('#', ''))
    
else:
    key = int(key)
    text += '#' * (key - len(text) % key)
    lenText = len(text)
    text = np.array(list(text)).reshape(key, lenText//key)

    ans = ''
    for i in range(lenText//key):
        ans += ''.join(list(text[:,i]))
    print(ans.replace('#', ''))
    
