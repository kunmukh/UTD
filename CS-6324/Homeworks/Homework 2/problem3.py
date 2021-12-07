# Name: Kunal Mukherjee
# Personal email: kunmukh@GMAIL.COM
# Date: 3/12/21
# File name: 
# Project name:

from decimal import Decimal


def main():

    group = [25, 35, 180]

    # part a,b
    for g in group:
        print("a: {}".format(1 - (Decimal((364/365)) ** g)))

    # part c
    for g in group:

        temp = 365/365
        for i in range(365 - g, 365):
            temp *= (i/365)

        a = 1 - Decimal(temp)

        print("b: {}".format(a))


if __name__ == '__main__':
    main()