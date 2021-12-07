# Name: Kunal Mukherjee
# Personal email: kunmukh@GMAIL.COM
# Date: 3/12/21
# File name:
# Project name:

from decimal import Decimal


def main():

    n = Decimal(128)

    t = Decimal(1)/ (Decimal(2) ** n)
    t = 1 - t
    t = t ** (2 ** n)
    t = 1 - t

    print(t)


if __name__ == '__main__':
    main()