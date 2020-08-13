/* 
# File: router.c
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
#include "router.h"
#include "routerRP.h"

// router server driver function
void * routerServer(void *vargp)
{
    //initialize random
    srand(time(NULL));

    char random[2];
    int _random = rand() % 100;
    char fileBaseName[17] = "routerServer.txt";

    sprintf(random, "%d", _random);
    strncat(fileName, random, strlen(random));
    strncat(fileName, fileBaseName+strlen(random), strlen(fileBaseName));

    printf("Thread : The output file is %s\n", fileName);

    // sleep for some time
	sleep(5);

    fptr = fopen(fileName, "a");    

    fprintf(fptr, "Thread: Printing from Thread \n");

    // start the client server
    int sockfd, connfd;
    socklen_t len;
	struct sockaddr_in servaddr, cli; 

	// socket create and verification 
	sockfd = socket(AF_INET, SOCK_STREAM, 0); 
	if (sockfd == -1)
	{ 
		fprintf(fptr, "Thread: socket creation failed...\n"); 
		exit(0); 
	} 
	else
		fprintf(fptr, "Thread: Socket successfully created..\n"); 
	bzero(&servaddr, sizeof(servaddr)); 

	// assign IP, PORT 
	servaddr.sin_family = AF_INET; 
	servaddr.sin_addr.s_addr = inet_addr(self.IP);; 
	servaddr.sin_port = htons(atoi(self.PORT)); 

	// Binding newly created socket to given IP and verification 
	if ((bind(sockfd, (SA*)&servaddr, sizeof(servaddr))) != 0)
	{ 
		fprintf(fptr, "Thread: socket bind failed...\n"); 
		exit(0); 
	} 
	else
		fprintf(fptr, "Thread: Socket successfully binded..\n"); 

	// Now server is ready to listen and verification 
	if ((listen(sockfd, 5)) != 0)
	{ 
		fprintf(fptr, "Thread: Listen failed...\n"); 
		exit(0); 
	} 
	else
		fprintf(fptr, "Thread: Server listening..\n");


    fclose(fptr);

	while(1)
	{
		fptr = fopen(fileName, "a");

        // if a request comes then handle the request
		// Accept the data packet from client and verification
		connfd = accept(sockfd, (SA*)&cli, &len);

		if (connfd < 0) 
		{ 
			fprintf(fptr, "Thread: server accept failed...\n");
		} 
		else
        {
			fprintf(fptr, "Thread: server accept the client...\n");

            // Function for chatting between client and server
            processRequestRouter(connfd, neighbours, &curr_num_neigh);
        }		

		// After chatting close the connection 
		close(connfd);

		// Server is still listening
		fprintf(fptr, "Thread: Server listening..\n");

		// put some extra line to show end of transaction
		fprintf(fptr, "\n\n");

        fclose(fptr);
		
	}

	// After chatting close the socket 
	close(sockfd);
}

// main driver program
int main(int argc, char const *argv[])
{    
    // get self info
    // print the current machine IP
	char * IP = getIP();
    strncpy(self.IP, IP, strlen(IP));

	// port number from user
	char PORT[10];
    sprintf(PORT, "%d" ,getPort());
    strncpy(self.PORT, PORT, strlen(PORT));

    printf("Self IP and Port: %s:%s\n",self.IP, self.PORT);

    // run server in thread to handle request
    // thread creation to ask for updated routing tables
	pthread_t thread_id; 
	pthread_create(&thread_id, NULL, routerServer, NULL); 
	printf("Routing Thread Created\n");

    // sleep for 10 sec so that router server may start
    sleep(10);

    // ask the user if they want to connect to a RP or a router
    int choice = 0;
    printf("What do you want to do 1>Connect RP 2>Connect Router(RP Group) 3>Send Message 4>Connect Router:\n");
    scanf("%d", &choice);
    
    while (choice != 1 || choice != 2 || choice != 3)
    {
        // user choice to join
        if (choice == 1 && isPartGroup == 0)
        {
            // Get RP info
            struct neighbour _temp;
            // ask the user for ip and port of the RP from user
            printf("ENTER RP router IP Port(192.168.1.1 8080):\n");
            scanf("%s %s", _temp.IP, _temp.PORT);

            // send join request to RP
            isPartGroup = sendJoin(_temp.IP, _temp.PORT, self.IP, self.PORT, 0, &RP);
            
        }
        else if (choice == 1 && isPartGroup != 0)
        {
            printf("You are already part of RP group %s:%s\n", RP.IP, RP.PORT);
        }

        // user wants to connect to a Router that is part of RP group
        if (choice == 2 && isPartGroup == 0)
        {
            // ask the router to ROUTER_JOIN

            // Get Router info-should be a neighbour
            struct neighbour _temp;
            // ask the user for ip and port of the RP from user
            printf("ENTER router IP Port(192.168.1.1 8080):\n");
            scanf("%s %s", _temp.IP, _temp.PORT);

            // send join request to RP
            isPartGroup = sendJoin(_temp.IP, _temp.PORT, self.IP, self.PORT, 1, &RP);


        }
        else if (choice == 2 && isPartGroup != 0)
        {
            printf("You are already part of RP group %s:%s\n", RP.IP, RP.PORT);
        }

        //user wants to send a message
        if (choice == 3)
        {
            // get the message
            // send a message to the group
            char message [MAX];

            // get the meaage from the user
            printf("Enter a message to send: ");

            // TODO: error handle scanf leaves behind a newline
            fgets(message,sizeof(message), stdin);
            bzero(message, sizeof(message));

            // get the new line and remove the end of line
            fgets(message,sizeof(message), stdin);
            message[strcspn(message, "\n")] = 0;
            
            // get the destination
            int choiceDest;
            
            // ask to send to a router or RP
            printf("DEST of message: 1> RP 2> Router 3>Neighbours\n");
            scanf("%d", &choiceDest);

            // want to send message to RP
            if (choiceDest == 1 && isPartGroup == 1)
            {
                // send message to RP to propogate
                sendMessage(message, RP.IP, RP.PORT);
            }
            else if (choiceDest == 1 && isPartGroup != 1)
            {
                printf("You are not part of any group. First join a group(option 1)\n");
            }
            // want to send it to a router
            if (choiceDest == 2)
            {
                struct neighbour _router;

                printf("ENTER router IP Port(192.168.1.1 8080):\n");
                scanf("%s %s", _router.IP, _router.PORT);

                // send message to router to router
                sendMessage(message, _router.IP, _router.PORT);
            }
            // want to send both and is part of group
            if (choiceDest == 3 && hasNeighbours == 1)
            {
                // send the message to all of my connected routers
                for (int i = 0; i < curr_num_neigh; i++)
                {
                    // send the meaage to all the neighbour
                    printf("Propagating broadcast message [%s] to neighbour %s:%s\n", 
                        message, neighbours[i].IP, neighbours[i].PORT);
                    
                    sendMessageNeigh(message, neighbours[i], 2);
                }
            }
            else if (choiceDest == 3 && hasNeighbours != 1)
            {
                printf("You do not have any neighbours\n");
            }
            
        }

        //user wants to connect to a router directly
        if (choice == 4)
        {
            // Get RP info
            struct neighbour _temp;
            // ask the user for ip and port of the RP from user
            printf("ENTER RP router IP Port(192.168.1.1 8080):\n");
            scanf("%s %s", _temp.IP, _temp.PORT);

            // send join request to RP
            sendJoin(_temp.IP, _temp.PORT, self.IP, self.PORT, 2, &RP);
        }

        // again ask the user what to do
        printf("What do you want to do 1>Connect RP 2>Connect Router 3>Send Message 4>Connect Router:\n");
        scanf("%d", &choice);
    }

    // wait for the thread to join -- never
    pthread_join(thread_id, NULL); 

    
	return 0;

}