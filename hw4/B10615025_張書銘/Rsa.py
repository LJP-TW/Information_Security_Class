#!/usr/bin/python3.8
import argparse
import time
import random
import math
import binascii

# Miller-Rabin Test
def _MRTest(n):
    # Randomly select number x which 1 < x < n
    random.seed(time.time())
    x = random.randrange(2, n)
    exp = n - 1

    # First, check x^exp equiv 1 (mod n)
    result = pow(x, exp, n)
    if result != 1:
        return False

    while exp % 2 == 0:
        exp = exp // 2
        result = pow(x, exp, n)
        if result == n - 1:
            return True
        elif result == 1:
            continue
        else:
            return False

    return True

# Run Miller-Rabin Test for i times
def MRTest(n, i):
    for j in range(i):
        result = _MRTest(n)
        if result == False:
            return False
    return True

# Get big prime
def GetBigPrime(bits):
    random.seed(time.time())
    while True:
        n = (1 << bits - 1) + (random.getrandbits(bits - 2) << 1) + 1
        if MRTest(n, 8):
            return n


def InitRSA(bits):
    # find p, q
    p = GetBigPrime(bits)
    while True:
        q = GetBigPrime(bits)
        if q != p:
            break
    
    n = p * q
    phin = (p - 1) * (q - 1)

    # Select e
    for e in range(3, phin, 2):
        result = math.gcd(e, phin)
        if result == 1:
            break

    d = pow(e, -1, phin)

    print('p: {}'.format(p))
    print('q: {}'.format(q))
    print('n: {}'.format(n))    
    print('e: {}'.format(e))
    print('d: {}'.format(d))
    return

# p: string
#    plaintext bits
# n: int
#    RSA mod N
# key: int
#    Public Key or Private Key
# Return ciphertext int array
def EncryptRSA(p, n, key):
    c = []

    nbits = len(bin(n)[2:])
    blocksize = 1
    while blocksize * 2 < nbits:
        blocksize *= 2

    # padding
    remain = len(p) % blocksize
    if remain != 0:
        padding = blocksize - remain
        p = p + '0' * padding

    _c = pow(padding, key, n)
    c.append(_c)

    for i in range(0, len(p), blocksize):
        _p = int(p[i:i+blocksize], 2)
        _c = pow(_p, key, n)
        c.append(_c)

        # print('{} {}:{}\n\n{}\n{}\n'.format(i, len(p[i:i+blocksize]), p[i:i+blocksize], _p, _c))
    
    return c

# c: string
#    ciphertext int array
# n: int
#    RSA mod N
# key: int
#    Public Key or Private Key
# P: int
#    Big prime P
# Q: int
#    Big prime Q
# Return plaintext int array
def DecryptRSA(c, n, key, P=0, Q=0, E=0):
    p = []

    if P == 0:
        for _c in c:
            _p = pow(_c, key, n)
            p.append(_p)
    else:
        # Using Chinese Remainder Theorem
        dP = pow(E, -1, P - 1)
        dQ = pow(E, -1, Q - 1)
        pInv = pow(P, -1, Q)

        for _c in c:
            m1 = pow(_c, dP, P)
            m2 = pow(_c, dQ, Q)
            u = ((m2 - m1) * pInv) % Q
            m = P * u + m1

            p.append(m)

    return p

if __name__ == '__main__':
    # Setting Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--action', choices=['init', 'encrypt', 'decrypt'], default='init')

    initgroup = parser.add_argument_group('init', 'when action is init')
    initgroup.add_argument('-b', '--bits', type=int)
    
    cryptogroup = parser.add_argument_group('crypto', 'when action is encrypt or decrypt')
    cryptogroup.add_argument('-f', '--file', help='plaintext or ciphertext file')
    cryptogroup.add_argument('-n', help='mod N', type=int)
    cryptogroup.add_argument('-k', '--key', help='e or d (public key/private key)', type=int)
    cryptogroup.add_argument('-o', '--outputfile', help='output file (default is rsa.out)', default='rsa.out')
    cryptogroup.add_argument('-P', help='big prime P from init, only using at decryption', type=int)
    cryptogroup.add_argument('-Q', help='big prime Q from init, only using at decryption', type=int)
    cryptogroup.add_argument('-E', help='another key, only using at decryption', type=int)
    args = parser.parse_args()

    if args.action == 'init':
        if args.bits == None:
            parser.error('-b: missing')
        InitRSA(args.bits)
    elif args.action == 'encrypt':
        if args.file == None:
            parser.error('-f: missing')
        elif args.n == None:
            parser.error('-n: missing')
        elif args.key == None:
            parser.error('-k: missing')

        with open(args.file) as f:
            text = f.read()

            # Convert strings    to bytes
            # Convert bytes      to hex string
            # Convert hex string to int
            # Convert int        to bin
            text = str.encode(text)
            text = binascii.hexlify(text)
            text = int(text, 16)
            text = bin(text)[2:]
            if len(text) % 8 != 0:
                text = '0' * (8 - len(text) % 8) + text
            c = EncryptRSA(text, args.n, args.key)

        with open(args.outputfile, 'w+') as f:
            for _c in c:
                f.write('{}\n'.format(_c))
    elif args.action == 'decrypt':
        if args.file == None:
            parser.error('-f: missing')
        elif args.n == None:
            parser.error('-n: missing')
        elif args.key == None:
            parser.error('-k: missing')

        c = []
        with open(args.file) as f:
            line = f.readline()
            while line:
                line = line[:-1]
                c.append(int(line))
                line = f.readline()

        if args.P != None and args.Q != None and args.E != None:
            p = DecryptRSA(c, args.n, args.key, args.P, args.Q, args.E)
        else:
            p = DecryptRSA(c, args.n, args.key)

        padding, p = p[0], p[1:]

        with open(args.outputfile, 'w+') as f:
            for _p in p[:-1]:
                # Convert int        to hex string
                # Convert hex string to bytes
                # Convert bytes      to strings
                _p = hex(_p)[2:]
                _p = '0' * (len(_p) % 2) + _p
                _p = bytes.fromhex(_p)
                _p = _p.decode('utf-8')
                f.write(_p)

            _p = p[-1] >> padding
            _p = hex(_p)[2:]
            _p = '0' * (len(_p) % 2) + _p
            _p = bytes.fromhex(_p)
            _p = _p.decode('utf-8')
            f.write(_p)


