/* 
# File: SHPR.c
# Class: CS 6390                                    # Instructor: Dr. Ravi Prakash
# Assignment: Advance Computer Networks             # Date started: 06/21/2020
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

// struct for neighbour router
// to contain IP and Port
struct neighbour{
	char IP[256];
	char PORT[256];
};

// number of neighbour
int n_neigh = 0;

// array of neighbours
struct neighbour neighbours[2];

// ask node name
char choiceNode;

// round number
int roundNum = 0;

// ask flag so that cycle does not form
int askFlag = 0;


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

	printf("IP of this router: %s\n", IPbuffer);

	return IPbuffer;
}

// function get Port
int getPort()
{
	int PORT;
	printf("What port would you want to use for protocol?\n");
	scanf("%d", &PORT);
	return PORT;
}

// function to get IP and Port of neighbours
void getIPandPortneigh(struct neighbour * neighbours, int n_neigh)
{
	// get the port and ip of the neighbours
	for (int i = 0; i < n_neigh; i++)
	{

		printf("Nighbour IP Port(192.168.1.1 8080):\n");
		scanf("%s %s", neighbours[i].IP, neighbours[i].PORT);

	}

}

/*// debug print
void printALL(struct neighbour * neighbours, int n_neigh, int PORT)
{
	printf("******DEBUG*****\n\n");
	// print all the info
	printf("PORT: %d\n", PORT);
	printf("Number of neighbours: %d\n", n_neigh);
	for (int i = 0; i < n_neigh; i++)
	{	
		printf("neigh: %d IP:%s PORT:%s\n",i, neighbours[i].IP, neighbours[i].PORT);
	}
}*/

// global constants and variable needed for the communiation
#define MAX 256
#define SA struct sockaddr
// Routing Vector
char NODE[5] = {'a','b','c','d','e'};
// self node vector
int routeVec[10];
// buffer for neighbours routevec
char neigh1Buff[MAX];
char neigh2Buff[MAX];
// flag to count the number neighbour
int neighbourRecv = 0;
// broken link seen flag
int brokenLink = 0;


// Function to send Routing tables to router asking 
void func(int sockfd) 
{ 
	char buff[MAX];
	char reqRouter;

	// infinite loop for chat 
	for (;;) { 
		bzero(buff, MAX); 

		// read the message from client and copy it in buffer 
		read(sockfd, buff, sizeof(buff));

		// get the requesting router
		reqRouter = buff[27];

		// set flag so that multiple cycles do not form in a round
		if (reqRouter == choiceNode-1)
		{
			askFlag = 1;
		}


		// print buffer which contains the client contents 
		printf("From client %c: %s", reqRouter, buff);

		// clear out the buffer
		bzero(buff, MAX);

		// copy route vec into buffer
		buff[0] = choiceNode;
		for (int i = 1; i < 11; i++)
		{
			buff[i] = routeVec[i-1];
			//posion reverse
			if (i % 2 == 0)
			{
				if (buff[i] == 2)
				{
					buff[i] = 16;
				}
			}
		}

		// print the sending message
		printf("\nTo Req Router %c: Router:%c", reqRouter, buff[0]);
		for (int i = 1; i < 10; i+=2)
		{
			printf(" %c %d ", buff[i], buff[i+1]);
			
		}
		printf("\n");

		// and send that buffer to client 
		write(sockfd, buff, sizeof(buff)); 

		printf("Message sent to client\n");
		
		break;
	} 
} 


// Function to requesting Routing Tbales from a chosen router
void func2(int sockfd, char * IP, char * PORT) 
{ 
	char buff[MAX]; 

	for (;;) 
	{ 
		bzero(buff, sizeof(buff)); 
		printf("Thread: Requesting Routing table from %s %s\n", IP, PORT); 
		
		char messageSent[] = " REQUESTING RT FOR Router: ";
		strncat(messageSent, &choiceNode, 1);

		write(sockfd, messageSent, sizeof(messageSent)); 
		bzero(buff, sizeof(buff)); 
		read(sockfd, buff, sizeof(buff)); 

		// print the receiving message
		printf("Thread: From Router %c:", buff[0]);
		for (int i = 1; i < 10; i+=2)
		{
			printf(" %c %d ", buff[i], buff[i+1]);
		}
		printf("\n");
		
		// if first neighbour received
		
		for (int i = 0; i < MAX; i++)
		{
			if (neighbourRecv == 0)
			{
				neigh1Buff[i] = buff[i];				
			}
			if (neighbourRecv == 1)
			{
				neigh2Buff[i] = buff[i];				
			}
		}
		neighbourRecv++;

		printf("Thread: Server Answer Processed\n");
		break;
	} 
}

// thread function requesting routing table
void *threadRoutingTableRequestB(void *vargp) 
{
	while(1)
	{		

		// sleep for some time
		sleep(30);		

		printf("Thread: Printing from Thread \n");
		//1> Request Routing Table from neighbours
		for (int i = 0; i < n_neigh; i++)
		{
			int sockfd;
			struct sockaddr_in servaddr;

			// socket create and varification 
			sockfd = socket(AF_INET, SOCK_STREAM, 0); 
			if (sockfd == -1)
			{ 
				printf("Thread: socket creation failed...\n"); 
				exit(0); 
			} 
			else
				printf("Thread: Socket successfully created..\n"); 
			bzero(&servaddr, sizeof(servaddr));

			// assign IP, PORT 
			servaddr.sin_family = AF_INET; 
			servaddr.sin_addr.s_addr = inet_addr(neighbours[i].IP); 
			servaddr.sin_port = htons(atoi(neighbours[i].PORT)); 

			// connect the client socket to server socket 
			if (connect(sockfd, (SA*)&servaddr, sizeof(servaddr)) != 0)
			{ 
				printf("Thread: connection with the server failed...\n"); 
				exit(0); 
			} 
			else
			{
				printf("Thread: connected to the server: %s %s\n", 
					neighbours[i].IP, neighbours[i].PORT);
			}

			// function for chat 
			func2(sockfd, neighbours[i].IP, neighbours[i].PORT); 

			// close the socket 
			close(sockfd);

			// say socket closed
			printf("Thread: Socket closed\n");
		}
		printf("Thread: All Routing table from neighbour received\n");

		// reset the received flag
		neighbourRecv = 0;

		// Update the routing table
		if(n_neigh == 1)
		{
			for (int i = 1; i < 10; i+=2)
			{
				if (routeVec[i] != 0 && 
					routeVec[i-1] == neigh1Buff[0] &&
					neigh1Buff[i+1] != 16)
				{
					routeVec[i] = neigh1Buff[i+1]+1;
					routeVec[i-1] = neigh1Buff[0];

					// if 16 reached, just incrementing
					if (routeVec[i] >= 16 && routeVec[i] <=18)
						routeVec[i] = 16;				
				}		
			}
		} 
		

		// print the routing table
		printf("\n\nThread: ***Current Updated Cost for RT Round:%d***\n", roundNum);
		
		for(int i = 1; i < 10; i+=2)
		{			
			printf("Thread: NODE:%c FROM %c COST %d \n", 
				NODE[i/2], routeVec[i-1], routeVec[i]);				
			
		}
		printf("Thread: ***Current Updated Cost for Routing Table***\n");	

		printf("Thread: Exiting...\n\n\n");

		// increment the routing number
		roundNum++;
	}

	return NULL; 
}

// thread function requesting routing table
void *threadRoutingTableRequest(void *vargp) 
{
	// sleep for some time
	sleep(5);

	printf("Thread: Printing from Thread \n");

	//1> Request Routing Table from neighbours
	for (int i = 0; i < n_neigh; i++)
	{
		int sockfd;
		struct sockaddr_in servaddr;

		// socket create and varification 
		sockfd = socket(AF_INET, SOCK_STREAM, 0); 
		if (sockfd == -1)
		{ 
			printf("Thread: socket creation failed...\n"); 
			exit(0); 
		} 
		else
			printf("Thread: Socket successfully created..\n"); 
		bzero(&servaddr, sizeof(servaddr));

		// assign IP, PORT 
		servaddr.sin_family = AF_INET; 
		servaddr.sin_addr.s_addr = inet_addr(neighbours[i].IP); 
		servaddr.sin_port = htons(atoi(neighbours[i].PORT)); 

		// connect the client socket to server socket 
		if (connect(sockfd, (SA*)&servaddr, sizeof(servaddr)) != 0)
		{ 
			printf("Thread: connection with the server failed...\n"); 
			exit(0); 
		} 
		else
		{
			printf("Thread: connected to the server: %s %s\n", 
				neighbours[i].IP, neighbours[i].PORT);
		}

		// function for chat 
		func2(sockfd, neighbours[i].IP, neighbours[i].PORT); 

		// close the socket 
		close(sockfd);

		// say socket closed
		printf("Thread: Socket closed\n");
	}
	printf("Thread: All Routing table from neighbour updated\n");

	// reset the received flag
	neighbourRecv = 0;

	
	// Update the routing table
	// if there is only one neighbour
	if(n_neigh == 1)
	{
		for (int i = 1; i < 10; i+=2)
		{
			if (routeVec[i] != 0 &&				
				routeVec[i-1] == neigh1Buff[0]
				&& neigh1Buff[i+1] != 16)
			{
				routeVec[i] = neigh1Buff[i+1]+1;
				routeVec[i-1] = neigh1Buff[0];

				// if 16 reached, just incrementing
				if (routeVec[i] >= 16 
					&& routeVec[i] <=18  
					&& brokenLink == 1)
					routeVec[i] = 16;
			}				
		}
	}
	// if there is more than one neighbour
	if (n_neigh == 2)
	{
		for (int i = 1; i < 10; i+=2)
		{
			if (routeVec[i] != 0)
			{
				// update the route of the best hop
				if (neigh1Buff[i+1] <= neigh2Buff[i+1] &&
					neigh1Buff[i+1] != 16)
				{
					if (routeVec[i-1] == neigh1Buff[0])
					{
						routeVec[i] = neigh1Buff[i+1]+1;
						routeVec[i-1] = neigh1Buff[0];
					}					
				} 
				else 
				{
					if (routeVec[i-1] == neigh2Buff[0] &&
						neigh2Buff[i+1] != 16)
					{
						routeVec[i] = neigh2Buff[i+1]+1;
						routeVec[i-1] = neigh2Buff[0];
					}
				}

				// if 16 reached, just incrementing
				if (routeVec[i] >= 16 && 
					routeVec[i] <=18 && 
					brokenLink == 1)
					routeVec[i] = 16;
			}				
		}
	}

	// broken link flag
	for (int i = 1; i < 10; i += 2)
	{
		if (neigh1Buff[i+1] >= 16)
		{
			if (choiceNode-1 == neigh1Buff[i-1])
			{
				if (brokenLink == 1)
				{
					routeVec[i-1] = neigh1Buff[0];
					routeVec[i] = 16;
				}
				brokenLink = 1;
			}
		}
		if (n_neigh == 2 && neigh2Buff[i+1] >= 16)
		{
			if (choiceNode-1 == neigh2Buff[i-1])
			{
				if (brokenLink == 1)
				{
					routeVec[i-1] = neigh2Buff[0];
					routeVec[i] = 16;
				}
				brokenLink = 1;
			}
		}

	}

	printf("\n\n\nThread: ***Current Updated Cost for RT Round:%d***\n", roundNum);
	// update the routing table
	for(int i = 1; i < 10; i+=2)
	{			
		printf("Thread: NODE:%c FROM %c COST %d \n", 
				NODE[i/2], routeVec[i-1], routeVec[i]);			
		
	}
	printf("Thread: ***Current Updated Cost for Routing Table***\n");	

	printf("Thread: Exiting...\n\n\n");

	// increment the routing number
	roundNum++;

	return NULL; 
}


// main driver program
int main(int argc, char const *argv[])
{
	// which router does this app represent	
	printf("Which Node does this IP represent(b,c,d,e): \n");
	scanf("%c", &choiceNode);

	// depending on the router choice update the routing vector
	switch (choiceNode)
	{
		case 'b':
			{
				int Vec[10] = {'a',1,'b',0,'c',1,'c',2,'c',3};
				for (int i = 0; i < 10; i++)
				{
					routeVec[i] = Vec[i];
				}
				break;
			}
		case 'c': 
			{
				int Vec[10] = {'b',2,'b',1,'c',0,'d',1,'d',2};
				for (int i = 0; i < 10; i++)
				{
					routeVec[i] = Vec[i];
				}
				break; 
			}
		case 'd': 
			{
				int Vec[10] = {'c',3,'c',2,'c',1,'d',0,'e',1};
				for (int i = 0; i < 10; i++)
				{
					routeVec[i] = Vec[i];
				}
				break;
			}
		case 'e': 
			{
				int Vec[10] = {'d',4,'d',3,'d',2,'d',1,'e',0};
				for (int i = 0; i < 10; i++)
				{
					routeVec[i] = Vec[i];
				}
				break;
			}
		default: 
			{
				printf("Wrong choice!!!\n");
				return -1;
			}
	}

	// print he current routing table
	printf("***Current Routing Table Round 0***\n");
	// update the routing table
	for(int i = 1; i < 10; i+=2)
	{			
		printf("NODE:%c from:%c %d \n", 
				NODE[i/2], routeVec[i-1], routeVec[i]);				
		
	}
	printf("***Current Routing Table Round 0***\n");

	// print the current machine IP
	char * IP = getIP();

	// port number
	int PORT = getPort();


	// get the number of neighbours
	printf("How many neighbours?:\n");
	scanf("%d", &n_neigh);

	
	// get IP and Port of neighbours
	getIPandPortneigh(neighbours, n_neigh);

	// create the server and send its vector tabel
	// Server
	int sockfd, connfd, len; 
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
	servaddr.sin_addr.s_addr = inet_addr(IP);; 
	servaddr.sin_port = htons(PORT); 

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

	// debug print info
	//printALL(neighbours, n_neigh, PORT);

	if (choiceNode == 'b')
	{
		// link to a broken
		printf("Link to A BROKEN Simulation\n");
		routeVec[1] = 16;

		// start a round
		printf("Start RIP:SPLIT HORZ POISON REV...[PRESS ANY KEY]");
		getchar();
		char _temp;
		scanf("%c", &_temp);		

		// thread creation to ask for updated routing tables
		pthread_t thread_id; 
	    pthread_create(&thread_id, NULL, threadRoutingTableRequestB, NULL); 
	    printf("Routing Thread Created\n");

	}

	// increment the routing number
	roundNum++;

	while(1)
	{
		// if a request comes then handle the request
		// Accept the data packet from client and verification
		connfd = accept(sockfd, (SA*)&cli, &len);
		if (connfd < 0) 
		{ 
			printf("server accept failed...\n"); 
			exit(0); 
		} 
		else
			printf("server accept the client...\n"); 

		// Function for chatting between client and server 
		func(connfd); 

		// After chatting close the connection 
		close(connfd);

		// Server is still listening
		printf("Server listening..\n");
		
		if (choiceNode != 'b' && askFlag == 1)
		{
			// wait for 30 sec some time and ask for update from neighbours
			// thread creation to ask for updated routing tables
			pthread_t thread_id; 
			pthread_create(&thread_id, NULL, threadRoutingTableRequest, NULL); 
			printf("Routing Thread Created\n");			

			askFlag = 0;
		}
		
	}

	// After chatting close the socket 
	close(sockfd);

	return 0;
}