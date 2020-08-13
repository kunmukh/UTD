/* 
# File: routerRP.h
# Class: CS 6390                                    # Instructor: Dr. Ravi Prakash
# Assignment: Advance Computer Networks             # Date started: 06/21/2020
# Programmer: Kunal Mukherjee                       # Date completed:
*/

#ifndef ROUTER_RP_H_
#define ROUTER_RP_H_

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
#include <time.h>


// MAX is a global value
#define MAX 256

// struct to contain the IP
// to contain IP and Port
struct neighbour{
	char IP[MAX];
	char PORT[MAX];
};

// variable to store self ip and port
struct neighbour self;

// variable to store neighbours ip and port
struct neighbour neighbours[10];
int curr_num_neigh = 0;

#define SA struct sockaddr


// a file to output the server mssage that is from thread
//open file sample.txt in write mode 
FILE *fptr;
// global variable to store the filename
char fileName[19];

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

// function to print the router's routing table
void printRouterGroup(int curr_num_neigh, struct neighbour * neighbours, int flagRouter)
{
	if (flagRouter == 0)
    {
        // Print the router in the group
        printf("Router in the group: \n");
        for (int i = 0; i < curr_num_neigh; i++)
        {
            printf("%d> %s:%s\n", i, neighbours[i].IP, neighbours[i].PORT);
        }
    }
    else
    {
        // Print the router in the group
        fprintf(fptr, "Thread: Router in the group: \n");
        for (int i = 0; i < curr_num_neigh; i++)
        {
            fprintf(fptr, "Thread: %d> %s:%s\n", i, neighbours[i].IP, neighbours[i].PORT);
        }

    }
    
}

// send join message to the RP
void sendMessageNeigh(char * messageREQ, struct neighbour neigh, int flagRouter)
{    
    sleep(5);

    if (flagRouter == 0 || flagRouter == 2)
    {        

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
            printf("socket successfully created..\n"); 
        
        bzero(&servaddr, sizeof(servaddr));

        // assign IP, PORT 
        servaddr.sin_family = AF_INET; 
        servaddr.sin_addr.s_addr = inet_addr(neigh.IP); 
        servaddr.sin_port = htons(atoi(neigh.PORT));

        // connect the client socket to server socket 
        if (connect(sockfd, (SA*)&servaddr, sizeof(servaddr)) != 0)
        { 
            printf("connection with the neighbour router failed...\n"); 
            exit(0);
        } 
        else
        {
            printf("connected to the router: %s:%s\n", neigh.IP, neigh.PORT);
        }
        
        // send the message
        if (flagRouter == 0)
        {
            char messageRP[] = "RP_MESSAGE";
            char messageSEND[MAX];

            bzero(messageSEND, sizeof(messageSEND));

            // create the meaage
            strncat(messageSEND, messageRP, strlen(messageRP));
            strncat(messageSEND, messageREQ, strlen(messageREQ));

            printf("Sending message [%s] to RP at %s:%s \n",messageREQ, neigh.IP, neigh.PORT);
            
            // send the message
            write(sockfd, messageSEND, sizeof(messageSEND));
            
            // close the socket 
            close(sockfd);
        }
        else
        {
            char messageRP[] = "MESSAGE";

            char messageSEND[MAX];

            bzero(messageSEND, sizeof(messageSEND));

            // create the meaage
            strncat(messageSEND, messageRP, strlen(messageRP));
            strncat(messageSEND, messageREQ, strlen(messageREQ));

            printf("Sending message [%s] to neighbour at %s:%s \n",messageREQ, neigh.IP, neigh.PORT);
            
            // send the message
            write(sockfd, messageSEND, sizeof(messageSEND));
            
            // close the socket 
            close(sockfd);
        }
    }
    else
    {
        int sockfd;
        struct sockaddr_in servaddr;

        // socket create and varification 
        sockfd = socket(AF_INET, SOCK_STREAM, 0); 
        if (sockfd == -1)
        { 
            fprintf(fptr, "Thread: socket creation failed...\n"); 
            exit(0); 
        } 
        else
            fprintf(fptr, "Thread: socket successfully created..\n"); 
        
        bzero(&servaddr, sizeof(servaddr));

        // assign IP, PORT 
        servaddr.sin_family = AF_INET; 
        servaddr.sin_addr.s_addr = inet_addr(neigh.IP); 
        servaddr.sin_port = htons(atoi(neigh.PORT));

        // connect the client socket to server socket 
        if (connect(sockfd, (SA*)&servaddr, sizeof(servaddr)) != 0)
        { 
            fprintf(fptr, "Thread: connection with the neighbour router failed...\n"); 
            exit(0);
        } 
        else
        {
            fprintf(fptr, "Thread: connected to the router: %s:%s\n", neigh.IP, neigh.PORT);
        }
        
        // send the message
        char messageRP[] = "RP_MESSAGE";
        char messageSEND[MAX];

        bzero(messageSEND, sizeof(messageSEND));

        // create the meaage
        strncat(messageSEND, messageRP, strlen(messageRP));
        strncat(messageSEND, messageREQ, strlen(messageREQ));

        fprintf(fptr, "Thread: Sending message [%s] to RP at %s:%s \n",messageREQ, neigh.IP, neigh.PORT);
        
        // send the message
        write(sockfd, messageSEND, sizeof(messageSEND));
        
        // close the socket 
        close(sockfd);

    }
    
}

// driver function to process request coming to the server
void processRequest(int sockfd, struct neighbour * neighbours, int * curr_num_neigh) 
{ 
	char buff[MAX];
    char IP[MAX];
    char PORT[MAX];

    char messageIP[] = "IP";
    char messagePORT[] = "PORT";

    char messageREQ[MAX];
	
	bzero(buff, MAX);
    bzero(messageREQ, sizeof(messageREQ));

	// read the message from client and copy it in buffer 
	read(sockfd, buff, sizeof(buff));

	// print buffer which contains the client contents 
	//printf("From client %s\n", buff);

    // if a router wants to join but does not know it is a router
    if (strstr(buff, "ROUTER_JOIN") != NULL)
    {
        char messageIP[] = "IP";
        char messagePORT[] = "PORT";
        char messageSUCCESS[] = "SUCCESS";

        char IP[MAX];
        char PORT[MAX];

        // get requesting router IP and Port
        // ask for IP
        write(sockfd, messageIP, sizeof(messageIP));

        // receive the IP
        bzero(IP, MAX); 

	    // read the message from client and copy it in buffer 
	    read(sockfd, IP, sizeof(IP));

        // ask for Port
        write(sockfd, messagePORT, sizeof(messagePORT));

        // receive the Port
        bzero(PORT, MAX); 

	    // read the message from client and copy it in buffer 
	    read(sockfd, PORT, sizeof(PORT));

        printf("Router %s:%s requested JOIN the group \n",IP,PORT);

        
        // add this IP and Port to graph
        //check to see if the IP and port has been added earlier
        int flagUnique = 1;
        for (int i = 0; i < *curr_num_neigh; i++)
        {
            if ((strcmp(neighbours[i].IP, IP) == 0) && 
                (strcmp(neighbours[i].PORT, PORT) == 0))
            {
                // set the unique flag to false
                flagUnique = 0;
                printf(" %s:%s already in the group\n" ,IP, PORT);
                break;
            }
        }

        if (flagUnique)
        {
            strncpy(neighbours[*curr_num_neigh].IP, IP, strlen(IP));
            strncpy(neighbours[*curr_num_neigh].PORT, PORT, strlen(PORT));

            *curr_num_neigh = *curr_num_neigh + 1;
        }

        // send succesful message
        write(sockfd, messageSUCCESS, sizeof(messageSUCCESS));

        //send BP router IP and PORT
        //TODO:fix
        char _IP[MAX];
        char _PORT[MAX];
        char _message[MAX];

        bzero(_IP, sizeof(_IP));
        bzero(_IP, sizeof(_PORT));
        bzero(_message, sizeof(_message));

        printf("Sending RP %s:%s to %s:%s\n", self.IP, self.PORT, IP, PORT);

        strcpy( _IP, self.IP);
        strcpy( _PORT, self.PORT);

	    read(sockfd, _message, sizeof(_message));
        printf("Message from %s:%s [%s]\n",IP, PORT, _message);

        write(sockfd, _IP, sizeof(_IP));

	    read(sockfd, _message, sizeof(_message));
        printf("Message from %s:%s [%s]\n",IP, PORT, _message);

        write(sockfd, _PORT, sizeof(_PORT));

    }

    // a router has asked to join
    else if (strstr(buff, "JOIN") != NULL)
    {
        // ask for IP
        write(sockfd, messageIP, sizeof(messageIP));

        // receive the IP
        bzero(IP, MAX); 

	    // read the message from client and copy it in buffer 
	    read(sockfd, IP, sizeof(IP));

        // ask for Port
        write(sockfd, messagePORT, sizeof(messagePORT));

        // receive the Port
        bzero(PORT, MAX); 

	    // read the message from client and copy it in buffer 
	    read(sockfd, PORT, sizeof(PORT));

        printf("Router %s:%s requested JOIN the group \n",IP,PORT);

        // add this IP and Port to graph
        //check to see if the IP and port has been added earlier
        int flagUnique = 1;
        for (int i = 0; i < *curr_num_neigh; i++)
        {
            if ((strcmp(neighbours[i].IP, IP) == 0) && 
                (strcmp(neighbours[i].PORT, PORT) == 0))
            {
                // set the unique flag to false
                flagUnique = 0;
                printf("Router %s:%s already in the group\n" ,IP,PORT);
                break;
            }
        }

        if (flagUnique)
        {
            // hack to dcxx machine issue -1
            strncpy(neighbours[*curr_num_neigh].IP, IP, strlen(IP));
            strncpy(neighbours[*curr_num_neigh].PORT, PORT, strlen(PORT));

            *curr_num_neigh = *curr_num_neigh + 1;
        }
        
    }
    
    // a router has asked to send a message
    if (strstr(buff, "MESSAGE") != NULL)
    {        
        strncpy(messageREQ, buff+strlen("MESSAGE"), strlen(buff));

        for (int i = 0; i < *curr_num_neigh; i++)
	    {
		    // send the meaage to all the neighbours
            printf("Sending this message to propoagte: [%s] to %s:%s\n", 
                messageREQ, neighbours[i].IP, neighbours[i].PORT);
            sendMessageNeigh(messageREQ, neighbours[i], 0);
	    }
    }
	
}


#endif