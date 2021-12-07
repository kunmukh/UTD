# Name: Kunal Mukherjee
# Personal email: kunmukh@GMAIL.COM
# Date: 3/8/21
# File name: 
# Project name:

import sympy
import copy


def RSA():
    N = 60529591

    # problem 6a
    p_list = list(sympy.sieve.primerange(0, N))
    q_list = copy.deepcopy(p_list)

    P, Q = None, None
    for p in p_list:
        for q in q_list:
            if p * q == N:
                print("{} * {} = {}".format(p, q, N))
                P, Q = p, q
        
        if P is not None:
            break

    # run it once 6073 * 9967 = 60529591
    P, Q = 6073, 9967
    print("P: {} Q: {}".format(P, Q))

    phi_n = (P-1) * (Q-1)
    print("Phi({}): {} ".format(N, phi_n))

    # problem 6b
    e = 31

    d = 0
    while True:
        temp = (e * d) % phi_n
        if temp == 1 and d < phi_n:
            print("d={}".format(d))
            break
        else:
            d += 1

    # problem 6c
    d = 29280751
    CTs = [10000, 20000, 30000, 40000, 50000, 60000]

    # compute M = C^d % n = (M^e % n)^d % n = M^(e*d) % n
    # M=CT^d % n = 10000^29280751 % 60529591 = 34910012
    # M=CT^d % n = 20000^29280751 % 60529591 = 33207991
    # M=CT^d % n = 30000^29280751 % 60529591 = 54348463
    # M=CT^d % n = 40000^29280751 % 60529591 = 31535938
    # M=CT^d % n = 50000^29280751 % 60529591 = 5844860
    # M=CT^d % n = 60000^29280751 % 60529591 = 46207307
    for CT in CTs:
        print("M=CT^d % n = {}^{} % {} = {}".format(CT, d, N, (CT ** d) % N))


def main():
    RSA()


if __name__ == '__main__':
    main()