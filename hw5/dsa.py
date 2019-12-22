#!/usr/bin/python3.8
import argparse
import time
import random
import hashlib

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

def generate():
    random.seed(time.time())
    q = GetBigPrime(160)

    # generate p
    while True:
        k = random.randint(pow(2, 1024-160-1), pow(2, 1024-160))
        p = k * q + 1
        if len(bin(p)) - 2 == 1024 and MRTest(p, 8):
            break

    # generate a such that pow(a, q, p) == 1
    while True:
        h = random.randint(2, p - 1)
        a = pow(h, (p-1)//q, p)
        if a > 1:
            break

    d = random.randint(1, q - 1)
    b = pow(a, d, p)

    return p, q, a, b, d

def sign(m, p, q, a, b, d):
    random.seed(time.time())
    sha1 = hashlib.sha1()

    k = random.randint(1, q - 1)
    invK = pow(k, -1, q)

    r = pow(a, k, p) % q
    sha1.update(m)
    h = int(sha1.hexdigest(), 16)
    s = ((h + d * r) * invK) % q
    return r, s

def verify(m, p, q, a, b, r, s):
    sha1 = hashlib.sha1()

    w = pow(s, -1, q)
    sha1.update(m)
    h = int(sha1.hexdigest(), 16)
    u1 = (w * h) % q
    u2 = (w * r) % q
    v = ((pow(a, u1, p) * pow(b, u2, p)) % p) % q

    if v == r:
        return True
    else:
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--action', choices=['generate', 'sign', 'verify'], default='generate')
    parser.add_argument('-k', '--keyfile', help='public key filename. If -a argument is \'generate\', the postfix of private key file is \'.pri\'. Default is \'dsakey\'', default='dsakey')
    parser.add_argument('-m', '--msg', help='the message which will be signed')
    parser.add_argument('-f', '--msgfile', help='the message file which will be signed')
    parser.add_argument('-s', '--signaturefile', default='msg.sig')
    args = parser.parse_args()

    if args.action == 'generate':
        p, q, a, b, d = generate()

        print('p: {}'.format(p))
        print('q: {}'.format(q))
        print('a: {}'.format(a))
        print('b: {}'.format(b))
        print('d: {}'.format(d))

        with open(args.keyfile, 'w+') as f:
            f.write('{}\n'.format(p))
            f.write('{}\n'.format(q))
            f.write('{}\n'.format(a))
            f.write('{}\n'.format(b))

        with open(args.keyfile + '.pri', 'w+') as f:
            f.write('{}\n'.format(d))

        print('public  key is stored at file {}'.format(args.keyfile))
        print('private key is stored at file {}'.format(args.keyfile + '.pri'))
        
    elif args.action == 'sign':
        if args.msg == None and args.msgfile == None:
            parser.error('Need to give message to sign by -m or -f')
        if args.msg != None and args.msgfile != None:
            parser.error('Cannot use both: -m and -f')

        if args.msg != None:
            m = args.msg
        elif args.msgfile != None:
            try:
                with open(args.msgfile) as f:
                    m = f.read()
            except IOError:
                parser.error('No such file: {}'.format(args.msgfile))
        else:
            parser.error('Unknown Error')

        try:
            with open(args.keyfile) as f:
                p = int(f.readline())
                q = int(f.readline())
                a = int(f.readline())
                b = int(f.readline())
        except IOError:
            parser.error('No such file: {}'.format(args.keyfile))

        try:
            with open(args.keyfile + '.pri') as f:
                d = int(f.readline())
        except IOError:
            parser.error('No such file: {}'.format(args.keyfile + '_pri'))

        r, s = sign(str.encode(m), p, q, a, b, d)

        print('r: {}'.format(r))
        print('s: {}'.format(s))

        with open(args.signaturefile, 'w+') as f:
            f.write('{}\n'.format(r))
            f.write('{}\n'.format(s))

        print('signature is stored at file {}'.format(args.signaturefile))

    elif args.action == 'verify':
        if args.msg == None and args.msgfile == None:
            parser.error('Need to give message to sign by -m or -f')
        if args.msg != None and args.msgfile != None:
            parser.error('Cannot use both: -m and -f')

        if args.msg != None:
            m = args.msg
        elif args.msgfile != None:
            try:
                with open(args.msgfile) as f:
                    m = f.read()
            except IOError:
                parser.error('No such file: {}'.format(args.msgfile))
        else:
            parser.error('Unknown Error')

        try:
            with open(args.keyfile) as f:
                p = int(f.readline())
                q = int(f.readline())
                a = int(f.readline())
                b = int(f.readline())
        except IOError:
            parser.error('No such file: {}'.format(args.keyfile))

        try:
            with open(args.signaturefile) as f:
                r = int(f.readline())
                s = int(f.readline())
        except IOError:
            parser.error('No such file: {}'.format(args.signaturefile))

        valid = verify(str.encode(m), p, q, a, b, r, s)

        print('valid: {}'.format(valid))

    else:
        parser.error('-a: invalid action')
