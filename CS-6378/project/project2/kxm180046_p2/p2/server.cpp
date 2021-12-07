/* 
# File: server.cpp
# Class: CS 6378                                    # Instructor: Dr. Ravi Prakash
# Assignment: Advance Operating System              # Date started: 03/14/2021
# Programmer: Kunal Mukherjee                       # Date completed:
*/

// add the libraries needed
#include <iostream>
#include <stdio.h>

#include "init-utils.h"
#include "work-utils-server.h"

#include <pthread.h>

using namespace std;

int main(void)
{
	// get the server number
	printf("Enter server number(0,1,2)\n");
	scanf("%c", &serverName);

	// print the current machine IP
	// todo: remove
	char * IP = getIP();

	// get the port number
	int PORT = getPort();

	printf("Running as server\n");

	printf("Server IP:%c:%s Port:%d\n", serverName, IP, PORT);

	// start the server creation process
	socklen_t len;
	int sockfd, connfd; 
	struct sockaddr_in servaddr, cli;

	// socket created and verification 
	sockfd = socket(AF_INET, SOCK_STREAM, 0); 
	if (sockfd == -1) 
	{ 
		printf("socket creation failed...\n"); 
		exit(0); 
	} 
	else
	{
		printf("Socket successfully created..\n"); 
	}

	// empty the servaddr
	bzero(&servaddr, sizeof(servaddr)); 
	
	// assign IP, PORT 
	servaddr.sin_family = AF_INET; 
	servaddr.sin_addr.s_addr =  inet_addr(IP); 
	servaddr.sin_port = htons(PORT);

	// Binding newly created socket to given IP and verification 
	if ((bind(sockfd, (SA*)&servaddr, sizeof(servaddr))) != 0) 
	{ 
		printf("socket bind failed...\n"); 
		exit(0); 
	} 
	else
	{
		printf("Socket successfully binded..\n"); 
	}

	// Now server is ready to listen and verification 
	if ((listen(sockfd, 5)) != 0) 
	{ 
		printf("Listen failed...\n"); 
		exit(0); 
	} 
	else
	{
		printf("Server listening..\n"); 
	}
	len = sizeof(cli);
	
	while(1)
	{		    	

		// Accept the data packet from client and verification 
		connfd = accept(sockfd, (SA*)&cli, &len); 
		if (connfd < 0) 
		{ 
			printf("server accept failed...\n"); 
			exit(0); 
		} 
		else
		{
			printf("server accept the client...\n"); 
		}
		// create a thread to handle this request
		pthread_t t;
		pthread_create(&t, NULL, serverWork, (void *)connfd);
		n_threads++;

		printf("Server work create...Num Threads:%d\n", n_threads);
	}		  
		
	// close the socket
	close(sockfd);

}