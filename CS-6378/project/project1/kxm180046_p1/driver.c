/* 
# File: driver.c
# Class: CS 6378                                    # Instructor: Dr. Ravi Prakash
# Assignment: Advance Operating System              # Date started: 02/06/2021
# Programmer: Kunal Mukherjee                       # Date completed:
*/

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

#include "init-utils.h"
#include "work-utils.h"

// ask node name: server or client
char choiceNode;

// number of neighbour
int n_server = 0;

// array of servers
struct neighbour servers[1];

// main driver program
int main(int argc, char const *argv[])
{

	// do you want to run as server or client	
	printf("Should the program run as a>server or b>client: \n");
	scanf("%c", &choiceNode);

	// print the current machine IP
	char * IP = getIP();

	// get the port number
	int PORT = getPort();

	// depending on the router choice update the routing vector
	switch (choiceNode)
	{
		// if the choice is to be a server
		case 'a':
			{
				printf("Running as server\n");

				printf("Server IP:%s Port:%d\n", IP, PORT);

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
			    	
			    	// Function for get the server work done 
			    	serverWork(connfd); 
			    	
			    	// close the connection
			    	close(connfd);

					printf("Server listening..\n");
			    }		  
			     
			    // close the socket
			    close(sockfd);
				break;
			}
		// if they selected to as client then work as one
		case 'b': 
			{
				printf("Running as client\n");

				printf("Client IP:%s Port:%d\n", IP, PORT);

				// get the number of servers
				n_server = 1;

				// get the IP and Port
				getIPandPortserver(servers, n_server);

				for (int i = 0; i < n_server; i++)
				{	
					printf("servers #1: %d IP:%s PORT:%s\n",i, servers[i].IP, servers[i].PORT);
				}

				int sockfd; 
			    struct sockaddr_in servaddr; 
			  
			    // socket create and varification 
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

			    bzero(&servaddr, sizeof(servaddr)); 
			  
			    // assign IP, PORT 
			    servaddr.sin_family = AF_INET; 
			    servaddr.sin_addr.s_addr = inet_addr(servers[0].IP); 
			    servaddr.sin_port = htons(atoi(servers[0].PORT)); 
			  
			    // connect the client socket to server socket 
			    if (connect(sockfd, (SA*)&servaddr, sizeof(servaddr)) != 0) 
			    { 
			        printf("connection with the server failed...\n"); 
			        exit(0); 
			    } 
			    else
			    {
			        printf("Connected to the server: %s %s\n", servers[0].IP, servers[0].PORT);
			    }
			  
			    // Function for get the client work done 
			    clientWork(sockfd); 
			  
			    // close the socket 
			    close(sockfd); 	
				break; 
			}
	}
	

	return 0;
}