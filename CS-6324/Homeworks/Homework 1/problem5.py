# Name: Kunal Mukherjee
# Personal email: kunmukh@GMAIL.COM
# Date: 2/11/21
# File name: 
# Project name:

import random
import os

RAND_STR_LEN = 17


def encrypt(PT, key):

    cipher_text = []
    for i, pt in enumerate(PT):
        x = (ord(pt) + ord(key[i])) % 26
        x += ord('A')
        cipher_text.append(chr(x))

    return "".join(cipher_text)


def decrypt(CT, key):
    orig_text = []
    for i, ct in enumerate(CT):
        x = (ord(ct) - ord(key[i])) % 26
        x += ord('A')
        orig_text.append(chr(x))

    y_dec = "".join(orig_text)
    # print("_y:  ", y_dec)

    plaintext_dec = makeY(y_dec, "decrypt")
    # print("_pt: ", plaintext_dec)
    # print("pt:  ", plaintext_dec[RAND_STR_LEN:])

    return plaintext_dec[RAND_STR_LEN:]


def makeY(x, option):
    _temp_y = x
    y = []
    for i, xi in enumerate(x):
        if 0 <= i <= 16:
            y.append(xi)
        else:
            if option == "encrypt":
                _y = (ord(x[i]) + ord(y[i - RAND_STR_LEN])) % 26
            else:
                _y = (ord(x[i]) - ord(_temp_y[i - RAND_STR_LEN])) % 26

            _y += ord('A')
            y.append(chr(_y))
    y = "".join(y)

    return y


def getRandomStr(length):

    # 17 byte random
    rand_byte = os.urandom(length)

    rand_str = []
    for b in rand_byte:
        val = b % 26
        val += ord('A')
        rand_str.append(chr(val))

    rand_str = "".join(rand_str)

    return rand_str


def recoverKEY(M1, CT1, CT2):
    print(" ")

    new_key = []

    for i, (xi, ci) in enumerate(zip(M1, CT1)):
        if i < RAND_STR_LEN:
            g = (ord(ci) - ord(M1[i])) % 26
            g += ord('A')
            new_key.append(chr(g))

        else:
            g = (ord(ci) - ord(M1[(i - RAND_STR_LEN) % RAND_STR_LEN])) % 26
            g += ord('A')
            new_key.append(chr(g))

    new_key = "".join(new_key)

    print("CT1:  ", CT1[0:RAND_STR_LEN], " ", CT1[RAND_STR_LEN:])
    print("M1:   ", M1[0:RAND_STR_LEN], " ", M1[RAND_STR_LEN:])
    print("-")
    print("KEY:  ", new_key[0:RAND_STR_LEN], " ", new_key[RAND_STR_LEN:])
    print("")

    plaintext_dec = decrypt(CT2, new_key)
    print("pt2: ", plaintext_dec)
    print("")


def main():

    # answer 5a,b
    plaintext1 = "ABCDEFGGHIJKLMNOPQRSTUVWXYZ"
    print("pt:   {}".format(plaintext1))

    KEY = [chr(int(random.uniform(0, 26)) + ord('A')) for _ in range(0, len(plaintext1)+RAND_STR_LEN)]
    print("key:  {}".format("".join(KEY)))

    print("")

    for i in range(3):
        rand_str = getRandomStr(RAND_STR_LEN)
        print("rnd str (len 17): {}".format(rand_str))

        x = rand_str + plaintext1
        print("x: {}".format(x))

        y = makeY(x, "encrypt")
        print("y: {}".format(y))

        ct = encrypt(y, KEY)
        print("ct:  ", ct)

        plaintext_dec = decrypt(ct, KEY)
        print("pt_dec: ", plaintext_dec)

        print("")


    # answer 5c
    plaintext1 = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    print("5c ******")
    KEY = [chr(int(random.uniform(0, 26)) + ord('A')) for _ in range(0, len(plaintext1) + RAND_STR_LEN)]
    print("org key  ", "".join(KEY), "\n")

    rand_str1 = getRandomStr(RAND_STR_LEN)
    print("rnd_str1 (len 17): {}".format(rand_str1))
    print("pt1: {}".format(plaintext1))
    x1 = rand_str1 + plaintext1
    print("M1(rnd_str1+pt1): {}".format(x1))
    y1 = makeY(x1, "encrypt")
    print("y1 {}".format(y1))
    ct1 = encrypt(y1, KEY)
    print("CT1: ", ct1)

    print("")

    plaintext2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    rand_str2 = getRandomStr(RAND_STR_LEN)
    print("rnd_str2 (len 17): {}".format(rand_str2))
    print("pt2: {}".format(plaintext2))
    x2 = rand_str2 + plaintext2
    print("M2(rnd_str2+pt2): {}".format(x2))
    y2 = makeY(x2, "encrypt")
    print("y2 {}".format(y2))
    ct2 = encrypt(y2, KEY)
    print("CT2: ", ct2)

    print("\nct1: {}\nct2: {}".format(ct1, ct2))
    recoverKEY(x1, ct1, ct2)


if __name__ == '__main__':
    main()