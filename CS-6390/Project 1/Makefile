# File: Makefile
# Class: CS 6390                                    # Instructor: Dr. Ravi Prakash
# Assignment: Advance Computer Networks             # Date started: 06/21/2020
# Programmer: Kunal Mukherjee                       # Date completed:

rip: RIP.o
		gcc -Wall -std=c99 -pthread RIP.o -o rip

RIP.o: RIP.c
		gcc -Wall -std=c99 -pthread -c RIP.c
		
sh: SH.o
		gcc -Wall -std=c99 -pthread SH.o -o sh

SH.o: SH.c
		gcc -Wall -std=c99 -pthread -c SH.c

shpr: SHPR.o
		gcc -Wall -std=c99 -pthread SHPR.o -o shpr

SHPR.o: SHPR.c
		gcc -Wall -std=c99 -pthread -c SHPR.c


clean:
		rm -f *.o *~ sh shpr rip