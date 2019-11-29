#coding=utf-8 
import random
from random import randint


def makeRandomNum(bits):  # w表示希望产生位数
    list = []
    list.append('1')  #最高位定为1
    for i in range(bits - 2):
        c = random.choice(['0', '1'])
        list.append(c)
    list.append('1') # 最低位定为1
    # print(list)
    res = int(''.join(list),2)
    return res


def bigMod(x, n, p):  # x^n mod P 递归求法 (x*x)^(n/2) mod P = ((x*x)mod P)^(n/2) mod P
    if n == 0:
        return 1
    res = bigMod((x * x) % p, n >> 1, p)
    if n & 1 != 0:
        res = (res * (x)) % p # x是较小数，x%p的结果就是本身
    return res

def MillerRabin(a, p):  # 优化点应该依旧不少，欢迎指正
    if bigMod(a, p - 1, p) == 1:
        u = (p-1) >> 1
        while (u & 1) == 0:
            t = bigMod(a, u, p)
            if t == 1:
                u = u >> 1
            else:
                if t == p - 1:
                    return True
                else:
                    return False
        else:
            t = bigMod(a, u, p)
            if t == 1 or t == p - 1:
                return True
            else:
                return False
    else:
        return False

def MillerRabinTest(p, k):  # k为测试次数，p为待测奇数
    while k > 0:
        a = randint(2, p - 1)
        if not MillerRabin(a, p):
            return False
        k = k - 1
    return True


def makePrime(bits):           # 产生512位素数
    while 1:
        d = makeRandomNum(bits)
        for i in range(50):  # 伪素数附近50个奇数都没有真素数的话，重新再产生一个伪素数
            u = MillerRabinTest(d+2*(i), 5)
            if u:
                b = d + 2*(i)
                break
            else:
                continue
        if u:
            return b
        else:
            continue