/* 
# File: routerRP.c
# Class: CS 6390                                    # Instructor: Dr. Ravi Prakash
# Assignment: Advance Computer Networks             # Date started: 06/21/2020
# Programmer: Kunal Mukherjee                       # Date completed:
*/

// header files
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include <unistd.h> 
#include <errno.h> 
#include <netdb.h> 
#include <sys/types.h> 
#include <sys/socket.h> 
#include <netinet/in.h> 
#include <arpa/inet.h>
#include <pthread.h>
#include <time.h>


// header file for router to contain auxillary functions
#include "routerRP.h"

// router server driver function
void * routerServerRP(void *vargp)
{
	// create the server
	// Server
	int sockfd, connfd;
	socklen_t len; 
	struct sockaddr_in servaddr, cli; 

	// socket create and verification 
	sockfd = socket(AF_INET, SOCK_STREAM, 0); 
	if (sockfd == -1)
	{ 
		printf("socket creation failed...\n"); 
		exit(0); 
	} 
	else
		printf("Socket successfully created..\n"); 
	bzero(&servaddr, sizeof(servaddr)); 

	// assign IP, PORT 
	servaddr.sin_family = AF_INET; 
	servaddr.sin_addr.s_addr = inet_addr(self.IP);; 
	servaddr.sin_port = htons(atoi(self.PORT)); 

	// Binding newly created socket to given IP and verification 
	if ((bind(sockfd, (SA*)&servaddr, sizeof(servaddr))) != 0)
	{ 
		printf("socket bind failed...\n"); 
		exit(0); 
	} 
	else
		printf("Socket successfully binded..\n"); 

	// Now server is ready to listen and verification 
	if ((listen(sockfd, 5)) != 0)
	{ 
		printf("Listen failed...\n"); 
		exit(0); 
	} 
	else
		printf("Server listening..\n");

	while(1)
	{
		// if a request comes then handle the request
		// Accept the data packet from client and verification
		connfd = accept(sockfd, (SA*)&cli, &len);
		if (connfd < 0) 
		{ 
			printf("server accept failed...\n");
		} 
		else
		{
			printf("server accept the client...\n");

			// Function for chatting between client and server
			processRequest(connfd, neighbours, &curr_num_neigh);
		}		

		// After chatting close the connection 
		close(connfd);

		// Server is still listening
		printf("Server listening..\n");

		printRouterGroup(curr_num_neigh, neighbours, 0);

		// put some extra line to show end of transaction
		printf("\n\n");
		
	}

	// After chatting close the socket 
	close(sockfd);
}

// main driver program
int main(int argc, char const *argv[])
{

    // print the current machine IP
	strcpy(self.IP, getIP());

	// port number from user
	int PORT = getPort();
	sprintf(self.PORT,"%d",PORT);
	
	printf("IP:PORT of RP is = %s:%s\n", self.IP,self.PORT);


    // create a server that listens to incoming message in 
    // specified IP and Port
    // If incoming message is JOIN
    // store the IP and Port of the connection 
    // run server in thread to handle request
    // thread creation to ask for updated routing tables
	pthread_t thread_id; 
	pthread_create(&thread_id, NULL, routerServerRP, NULL); 
	printf("Routing Thread Created\n");

	// wait for the thread to join -- never
    pthread_join(thread_id, NULL);
    

	return 0;

}