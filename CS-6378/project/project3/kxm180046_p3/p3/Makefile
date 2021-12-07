# File: Makefile
# Class: CS 6378                                    # Instructor: Dr. Ravi Prakash
# Assignment: Advance Operating System              # Date started: 03/14/2021
# Programmer: Kunal Mukherjee                       # Date completed:

CC=g++
CFLAG=-Wall -g -std=c++11 -pthread

all: server client

server: server.o
		$(CC) $(CFLAG) $< -o $@

server.o: server.cpp init-utils.h work-utils-server.h
		$(CC) $(CFLAG) -c $<

client: client.o
		$(CC) $(CFLAG) $< -o $@

client.o: client.cpp init-utils.h work-utils-client.h
		$(CC) $(CFLAG) -c $<

clean:
		rm -rf *.o *~ server client *.gch