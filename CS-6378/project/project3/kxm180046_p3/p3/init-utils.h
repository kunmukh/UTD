/* 
# File: init-utils.c
# Class: CS 6378                                    # Instructor: Dr. Ravi Prakash
# Assignment: Advance Operating System              # Date started: 03/14/2021
# Programmer: Kunal Mukherjee                       # Date completed:
*/
#ifndef INIT_UTILS_H
#define INIT_UTILS_H

// header files
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h> 
#include <errno.h> 
#include <netdb.h> 
#include <sys/types.h> 
#include <sys/socket.h> 
#include <netinet/in.h> 
#include <arpa/inet.h>
#include <pthread.h>

#include <ctype.h>
#include <string>
#include <iostream>
#include <fstream>

#define MAX_FUNC(a,b) (((a)<(b))?(a):(b))


// struct for neighbour router
// to contain IP and Port
struct neighbour{
	char IP[256];
	char PORT[256];
};


// get the server number
char serverName;


// Returns hostname for the local computer 
void checkHostName(int hostname) 
{ 
    if (hostname == -1) 
    { 
        perror("gethostname"); 
        exit(1); 
    } 
}
  

// Returns host information corresponding to host name 
void checkHostEntry(struct hostent * hostentry) 
{ 
    if (hostentry == NULL) 
    { 
        perror("gethostbyname"); 
        exit(1); 
    }
}


// function to print the IP
char * getIP()
{
	char hostbuffer[256];
	int hostname;
	char *IPbuffer; 
    struct hostent *host_entry;

    // To retrieve hostname
    hostname = gethostname(hostbuffer, sizeof(hostbuffer)); 
    checkHostName(hostname); 

	// To retrieve host information 
    host_entry = gethostbyname(hostbuffer); 
    checkHostEntry(host_entry); 

	// To convert an Internet network 
    // address into ASCII string 
    IPbuffer = inet_ntoa(*((struct in_addr*) 
                           host_entry->h_addr_list[0])); 

	printf("IP of this node: %s\n", IPbuffer);

	return IPbuffer;
}


// function get Port
int getPort()
{
	int PORT;
	printf("What port would you want to use for protocol?\n");
	// get the port 
	scanf("%d", &PORT);

	if ((PORT > 3000) && (PORT < 65000))
	{
		return PORT;
	}
	else
	{
		printf("Error in PORT value. Need to be in range (3000, 65000)\n");
		exit(-1);
	}
	
}


// function to get IP and Port of servers
void getIPandPortNeighbour(struct neighbour * servers, int n_server, std::string fname)
{
	std::ifstream configFile (fname);

	// get the port and ip of the servers
	for (int i = 0; i < n_server; i++)
	{
		configFile >> servers[i].IP >> servers[i].PORT;
	}

	configFile.close();

	/*// get the port and ip of the servers
	for (int i = 0; i < n_server; i++)
	{
		printf("Enter IP Port(e.g. 192.168.1.1 8080) for neighbour %d:\n", i+1);
		scanf("%s %s", servers[i].IP, servers[i].PORT);
	}*/
}


// debug print
void printALLNeighbour(struct neighbour * servers, int n_server, char * IP, int PORT)
{
	printf("\n\n******DEBUG*****");
	// print all the info
	printf("Current IP:PORT: %s:%d\n",IP, PORT);
	printf("Number of neighbours: %d\n", n_server);
	for (int i = 0; i < n_server; i++)
	{	
		printf("neighbour: %d IP:%s PORT:%s\n",i, servers[i].IP, servers[i].PORT);
	}
	printf("******DEBUG*****\n\n");
}

#endif