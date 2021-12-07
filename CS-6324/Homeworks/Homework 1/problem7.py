# Name: Kunal Mukherjee
# Personal email: kunmukh@GMAIL.COM
# Date: 2/5/21
# File name: 
# Project name:

import random


# repeat the key in cyclic manner
# until it matches the length
def generateKey(string, key):
    key = list(key)
    if len(string) == len(key):
        return (key)
    else:
        for i in range(len(string) - len(key)):
            key.append(key[i % len(key)])

    return "".join(key)


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

    return "".join(orig_text)


def main():

    tmp1 = ['A' for _ in range(0, 50)]
    tmp2 = ['A' for _ in range(0, 50)]

    PT1 = []
    for t in tmp1+tmp2:
        PT1.append(t)

    #PT1 = ['A' for _ in range(0, 100)]
    print("M1:  ", "".join(PT1))

    _key1 = [chr(int(random.uniform(0, 26))+ord('A')) for _ in range(0, 50)]
    KEY1 = [key for key in generateKey(PT1, _key1)]
    print("key: ", "".join(KEY1[0:50]))

    ct1 = encrypt(PT1, KEY1)
    print("ct:  ", ct1)
    print("ct[0:50] =   ", ct1[0:50])
    print("ct[51:100] = ", ct1[50:100])

    pt1 = decrypt(ct1, KEY1)
    print("pt:  ", pt1)

    print("\n\n")

    PT2 = "ABCD"*25
    print("M2:  ", "".join(PT2))

    KEY2 = KEY1

    '''KEY2=[]
    for c1 in ct1:
        tmp = (ord(c1) - ord('Z')) % 26
        tmp += ord('A')
        KEY2.append(chr(tmp))'''

    print("key: ", "".join(KEY2[0:50]))

    ct2 = encrypt(PT2, KEY2)
    print("ct:  ", ct2)
    print("ct[0:50] =   ", ct2[0:50])
    print("ct[51:100] = ", ct2[50:100])

    pt2 = decrypt(ct2, KEY2)
    print("pt:  ", pt2)


if __name__ == '__main__':
    main()
