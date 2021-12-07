# File: Makefile
# Class: CS 6378                                    # Instructor: Dr. Ravi Prakash
# Assignment: Advance Operating System              # Date started: 02/06/2021
# Programmer: Kunal Mukherjee                       # Date completed:

driver: driver.o
		gcc -Wall -std=c99 driver.o -o driver

driver.o: driver.c init-utils.h work-utils.h
		gcc -Wall -std=c99 -c driver.c

clean:
		rm -rf *.o *~ driver *.gch D1copy