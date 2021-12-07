# Name: Kunal Mukherjee
# Personal email: kunmukh@GMAIL.COM
# Date: 3/8/21
# File name: 
# Project name:
import math
import copy
import sympy
from decimal import Decimal

def ElGamal():
    p = 96737
    # gcd(e, p) = 1 for every element e
    Z_p = []

    # compute Z_p
    for e in range(p):
        if math.gcd(e, p) == 1:
            Z_p.append(e)

    Z_p.sort()

    print("len Zp: {} isPrime({}):{}".format(len(Z_p), p, sympy.isprime(p)))

    # find generator
    g = 0
    _g_list = list(sympy.sieve.primerange(0, p))

    for _g in _g_list:
        _Z_p = []

        for i in range(0, len(Z_p)):
            _Z_p.append((_g ** i) % p)

        _Z_p.sort()

        if Z_p == _Z_p and _g != 1:
            g = _g
            break
        else:
            print("{}/{} g not found".format(_g, len(_g_list)))

    # get the g
    # a> g = 3
    g = 3
    print("g= {}".format(g))

    # b> find x = 90620
    x = 0
    for _x in range(0, len(Z_p) - 1):
        if (g ** _x) % p == 90307:
            x = _x
            print("x: {}".format(_x))

    # c> decryption of El Gamal
    CTs = [[5000, 5001], [10000, 20000], [30000, 40000], [50000, 60000],
           [70000, 80000], [90000, 100000]]

    # Dr. Kim method
    # CT: [5000, 5001] = 46636
    # CT: [10000, 20000] = 18895
    # CT: [30000, 40000] = 37790
    # CT: [50000, 60000] = 56685
    # CT: [70000, 80000] = 75580
    # CT: [90000, 100000] = 94475
    for ct in CTs:
        # compute z
        for z in range(len(Z_p)):
            if (x * z) % p == 1:
                M = (ct[1] * z) % p
                print("Professor: CT: {} = {}".format(ct, M))

    # CT: [5000, 5001] = 85101
    # CT: [10000, 20000] = 4996
    # CT: [30000, 40000] = 31532
    # CT: [50000, 60000] = 28134
    # CT: [70000, 80000] = 51546
    # CT: [90000, 100000] = 46927
    for ct in CTs:
        # compute s = C1^x
        # M = s^-1 * C2
        s = (ct[0] ** x) % p

        s_i = 0
        while True:
            temp = (s * s_i) % p
            if temp == 1 and s_i < p:
                # print("d={}".format(s_i))
                break
            else:
                s_i += 1

        M = (ct[1] * s_i) % p
        print("Wiki: CT: {} = {}".format(ct, M))


def main():
    ElGamal()


if __name__ == '__main__':
    main()