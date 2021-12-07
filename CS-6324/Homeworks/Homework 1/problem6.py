# Name: Kunal Mukherjee
# Personal email: kunmukh@GMAIL.COM
# Date: 2/5/21
# File name: 
# Project name:

import numpy as np


def main():

    p = [i for i in range(1, 7)]
    k = [i for i in range(1, 7)]

    table = np.empty([6, 6])

    for i, pi in enumerate(p):
        for j, kj in enumerate(k):
            # print("i:{} j:{} pi:{} kj:{}".format(i, j, pi, kj))
            table[i, j] = (pi * kj) % 13

    print("table for PT x K\n", table.round(decimals=0), "\n")

    # problem 1
    # select the table where p = 5, 6
    table_1 = table[np.ix_([4, 5], [0, 1, 2, 3, 4, 5])]

    print("table for PT=5,6\n", table_1, "\n")

    uniqueVal= np.unique(table_1)

    CT_need = []

    # unique cipher text
    for val in uniqueVal:
        PT = np.where(table_1 == val)[0]+5
        K = np.where(table_1 == val)[1]+1

        if K.shape[0] == 1:
            print("CT:{} PT:{} K:{}".format(val, PT, K))
            CT_need.append(val)

    print("For CT {} we can guess the value of M or PT\n\n".format(CT_need))

    # problem 2
    CT = [i for i in range(1, 13)]
    PT = [i for i in range(1, 7)]

    for i, pt in enumerate(PT):
        for j, ct in enumerate(CT):

            _pt, _k = np.where(table == ct)

            total = len(_pt)

            count = 0
            for _pti in _pt:
                if _pti+1 == pt:
                    count = count + 1

            try:
                p_PT_and_CT = np.round(count/36., 2)
                p_CT = np.round(total/36., 2)
                print("Pr[PT={} | CT={}] = {} / {} = {}".format(pt, ct,
                                                                p_PT_and_CT,
                                                                p_CT,
                                                                (count/36.)/(total/36.)))
            except ZeroDivisionError:
                print("Pr[PT={} | CT={}] = {} / {} = {}".format(pt, ct, 0, 0, 0))


if __name__ == '__main__':
    main()
