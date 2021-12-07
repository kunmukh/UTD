# Name: Kunal Mukherjee
# Personal email: kunmukh@GMAIL.COM
# Date: 2/5/21
# File name: 
# Project name:

# used for bytes packing
import codecs
# used for random bits
import os
import random

IV = b''
i_PRGA = 0
j_PRGA = 0


def KSA(key):
    '''
    Key-scheduling algorithm (KSA) (wikipedia)
    for i from 0 to 255
        S[i] := i
    endfor
    j := 0
    for i from 0 to 255
        j := (j + S[i] + key[i mod keylength]) mod 256
        swap values of S[i] and S[j]
    endfor
    '''

    global IV

    key_len = len(key)

    S = [i for i in IV]

    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_len]) % 256
        S[i], S[j] = S[j], S[i]

    return S


def PRGA(S):
    '''
    Psudo Random Generation Algorithm (from wikipedia):
    i := 0
    j := 0
    while GeneratingOutput:
        i := (i + 1) mod 256
        j := (j + S[i]) mod 256
        swap values of S[i] and S[j]
        K := S[(S[i] + S[j]) mod 256]
        output K
    endwhile
    '''

    global i_PRGA, j_PRGA

    while True:
        i_PRGA = (i_PRGA + 1) % 256
        j_PRGA = (j_PRGA + S[i_PRGA]) % 256

        S[i_PRGA], S[j_PRGA] = S[j_PRGA], S[i_PRGA]  # swap values
        K = S[(S[i_PRGA] + S[j_PRGA]) % 256]
        return K


def encrypt(pt, key):
    global i_PRGA, j_PRGA
    i_PRGA = 0
    j_PRGA = 0

    # convert the each plaintext character to unicode
    pt = [ord(p) for p in pt]
    key = [c for c in key]

    # drop the first 3072 bytes
    for i in range(3072):
        keystream = PRGA(KSA(key))

    ct = []
    for _pt in pt:
        val = ("%02X" % (_pt ^ keystream))
        ct.append(val)

    # create a string from the hex array
    ct = ''.join(ct)

    return ct


def decrypt(ct, key):

    global i_PRGA, j_PRGA
    i_PRGA = 0
    j_PRGA = 0

    # convert hex string to bytes
    ct = codecs.decode(ct, 'hex_codec')
    key = [c for c in key]

    # drop the first 3072 bytes
    for i in range(3072):
        keystream = PRGA(KSA(key))

    # decrypt
    pt = []
    for _ct in ct:
        val = ("%02X" % (_ct ^ keystream))
        pt.append(val)

    # create the hex string
    pt = ''.join(pt)

    # convert the hex to bytes -> convert it to utd-8 string
    return codecs.decode(pt, 'hex_codec').decode('utf-8')


def main():

    global IV

    # key can be between 16 - 32 bytes
    # random key is generated
    key = os.urandom(random.randint(16, 32))
    # 256 byte IV
    IV = os.urandom(256)

    plaintext = 'Finally Done with CS6324 Homework'

    print('key: ', key)
    print('IV: ', IV)
    print('pt: ', plaintext)

    ciphertext = encrypt(plaintext, key)
    print('ct: ', ciphertext)

    # final output
    pt_1 = decrypt(encrypt(plaintext, key), key)
    print('pt: ', pt_1)


if __name__ == '__main__':
    main()