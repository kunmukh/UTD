# File: Makefile
# Class: CS 6390                                    # Instructor: Dr. Ravi Prakash
# Assignment: Advance Computer Networks             # Date started: 07/24/2020
# Programmer: Kunal Mukherjee                       # Date completed:

routerRP: routerRP.o
		gcc -Wall -std=c99 -pthread -o routerRP routerRP.o

routerRP.o: routerRP.c routerRP.h
		gcc -Wall -std=c99 -c routerRP.c

router: router.o
		gcc -Wall -std=c99 -pthread -o router router.o

router.o: router.c router.h  routerRP.h
		gcc -Wall -std=c99 -c router.c

clean:
		rm -f *.o *~ routerRP router *.txt