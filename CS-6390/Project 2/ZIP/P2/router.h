/* 
# File: router.h
# Class: CS 6390                                    # Instructor: Dr. Ravi Prakash
# Assignment: Advance Computer Networks             # Date started: 06/21/2020
# Programmer: Kunal Mukherjee                       # Date completed:
*/

#ifndef ROUTER_H_
#define ROUTER_H_

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


#include "routerRP.h"

#define SA struct sockaddr

//gloabl variables

// variable to store RP ip and port
struct neighbour RP;

// flag
int isPartGroup = 0;
int hasNeighbours = 0;

// send "JOIN" message to RP
int join(int sockfd, char * IP, char * PORT, char * selfIP, char * selfPORT, int flagRouter, struct neighbour * RP)
{
    char buff[MAX];
	
    // initialize the buffer
	bzero(buff, sizeof(buff));
		
	char messageSent[12];
    bzero(messageSent, sizeof(messageSent));
    
    if (flagRouter == 0)
    {
        printf("Send 'JOIN' message to RP at %s:%s \n", IP, PORT); 
        strncat(messageSent,"JOIN", strlen("JOIN"));
    }
    else if (flagRouter == 1)
    {
        printf("Send 'ROUTER_JOIN' message to router at %s:%s to join RP\n", IP, PORT); 
        strncat(messageSent,"ROUTER_JOIN", strlen("ROUTER_JOIN"));
    }
    else
    {
        printf("Send 'DIRECT_ROUTER_JOIN' message to router at %s:%s to join it\n", IP, PORT); 
        strncat(messageSent,"DIRECT_ROUTER_JOIN", strlen("DIRECT_ROUTER_JOIN"));
    }
    

    // send the meaage to the RP server
	write(sockfd, messageSent, sizeof(messageSent));

    // receive message
    // initialize the buffer
	bzero(buff, sizeof(buff));

    // read the message from client and copy it in buffer 
	read(sockfd, buff, sizeof(buff));

    // print buffer which contains the client contents 
	printf("From client %s\n", buff);

    // a router has asked to join
    if (strstr(buff, "IP") != NULL)
    {
        printf("IP:%s sent to RP router\n", selfIP);
        char _tempIP[MAX];
        strcpy(_tempIP, selfIP);
        write(sockfd, _tempIP, sizeof(_tempIP));
    }else
    {
       return 0;
    }

    // initialize the buffer
	bzero(buff, sizeof(buff));

    // read the message from client and copy it in buffer 
	read(sockfd, buff, sizeof(buff));

    // print buffer which contains the client contents 
	printf("From client %s\n", buff);

    // a router has asked to join
    if (strstr(buff, "PORT") != NULL)
    {
        printf("PORT:%s sent to RP router\n", selfPORT);
        char _tempPORT[MAX];
        strcpy(_tempPORT, selfPORT);
        write(sockfd, _tempPORT, sizeof(_tempPORT));
    }else
    {
        return 0;
    }

    
    if (flagRouter == 0)
    {
        strcpy(RP->IP, IP);
        strcpy(RP->PORT, PORT);
        
    }
    else if (flagRouter == 1)
    {
        // read the message from client and copy it in buffer 
	    read(sockfd, buff, sizeof(buff));

        if (strstr(buff, "SUCCESS") != NULL)
        {
            char _IP[MAX];
            char _PORT[MAX];

            bzero(_IP, sizeof(_IP));
            bzero(_IP, sizeof(_PORT));

            write(sockfd, "WANT_RP_IP", sizeof("WANT_RP_IP"));

            // read the message from client and copy it in buffer 
            read(sockfd, _IP, sizeof(_IP));

            write(sockfd, "WANT_RP_PORT", sizeof("WANT_RP_PORT"));

            // read the message from client and copy it in buffer 
            read(sockfd, _PORT, sizeof(_PORT));

            strcpy(RP->IP, _IP);
            strcpy(RP->PORT, _PORT);

            // print buffer which contains the client contents
            printf("From client the IP of RP %s:%s\n", RP->IP, RP->PORT);

        }else
        {
            printf("Message from router [%s]\n", buff);
            return 0;
        }
    }
    
    return 1;    

}

// send join message to the RP
int sendJoin(char * IP, char * PORT, char * selfIP, char * selfPORT, int flagRouter, struct neighbour * RP)
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
	servaddr.sin_addr.s_addr = inet_addr(IP); 
	servaddr.sin_port = htons(atoi(PORT));

	// connect the client socket to server socket 
	if (connect(sockfd, (SA*)&servaddr, sizeof(servaddr)) != 0)
	{ 
		printf("connection with the RP failed...\n"); 
		exit(0); 
	} 
	else
	{
		printf("connected to the RP: %s %s\n", IP, PORT);
	}
	
    // function for chat 
	int status = join(sockfd, IP, PORT, selfIP, selfPORT, flagRouter, RP); 
	
    // close the socket 
	close(sockfd);

    return status;
}

// send message to all the neighbours
void sendMessage(char * message, char * IP, char * PORT)
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
	servaddr.sin_addr.s_addr = inet_addr(IP); 
	servaddr.sin_port = htons(atoi(PORT));

	// connect the client socket to server socket 
	if (connect(sockfd, (SA*)&servaddr, sizeof(servaddr)) != 0)
	{ 
		printf("connection with the RP failed...\n"); 
		exit(0); 
	} 
	else
	{
		printf("connected to the RP: %s %s\n", IP, PORT);
	}
	
    // function for chat 
	char buff[MAX];
    char messageSent[] = "MESSAGE";

    // initialize the buffer
	bzero(buff, sizeof(buff));

    // create the meaage
    strncat(buff, messageSent, strlen(messageSent));
    strncat(buff, message, strlen(message));

	printf("Sending message [%s] to RP at %s:%s \n",message, IP, PORT);

    // send the meaage to the RP server
	write(sockfd, buff, sizeof(buff));
	
    // close the socket 
	close(sockfd);
}

// driver program to take care of requests coming to router server
void processRequestRouter(int sockfd, struct neighbour * neighbours, int * curr_num_neigh) 
{ 
	char buff[MAX];
    char message[MAX];
	
	bzero(buff, sizeof(buff));
    bzero(message, sizeof(message));

	// read the message from client and copy it in buffer 
	read(sockfd, buff, sizeof(buff));

	// print buffer which contains the client contents 
	//fprintf(fptr, "Thread: From client %s\n", buff);

    // RP has sent a message to propagate
    if (strstr(buff, "RP_MESSAGE") != NULL)
    {
        strncpy(message, buff+sizeof("RP_MESSAG"), sizeof(buff));
        fprintf(fptr, "Thread: Message broadcasted from RP: [%s]\n", message);

        //todo:fix
        fprintf(fptr, "Thread: current router group\n");
        printRouterGroup(*curr_num_neigh, neighbours, 1);

        // send the message to all of my connected routers
        for (int i = 0; i < *curr_num_neigh; i++)
	    {
		    // send the meaage to all the neighbour
            fprintf(fptr, "Thread: Propagating broadcast message from RP to [%s] %s:%s\n", 
                message, neighbours[i].IP, neighbours[i].PORT);
            
            sendMessageNeigh(message, neighbours[i], 1);
	    }
        
    }

    // a normal router has sent a message
    else if (strstr(buff, "MESSAGE") != NULL)
    {
        strncpy(message, buff+sizeof("MESSAG"), sizeof(buff));
        fprintf(fptr, "Thread: Message broadcasted from a router: [%s]\n", message);
    }

    // a normal router wants to join thsi router as a neighbour
    else if (strstr(buff, "DIRECT_ROUTE") != NULL)
    {
        char messageIP[] = "IP";
        char messagePORT[] = "PORT";

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

        fprintf(fptr,"Thread: Router %s:%s requested JOIN the router \n",IP,PORT);

        
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
                fprintf(fptr, "Thread: %s:%s already in the router\n" ,IP, PORT);
                break;
            }
        }

        if (flagUnique)
        {
            strncpy(neighbours[*curr_num_neigh].IP, IP, strlen(IP));
            strncpy(neighbours[*curr_num_neigh].PORT, PORT, strlen(PORT));

            *curr_num_neigh = *curr_num_neigh + 1;

            hasNeighbours = 1;
        }

    }

    // a normal router wants to join RP group
    else if (strstr(buff, "ROUTER_JOIN") != NULL)
    {
        char messageIP[] = "IP";
        char messagePORT[] = "PORT";
        char messageFAILED[] = "FAILED-This router not part of group";
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

        fprintf(fptr,"Thread: Router %s:%s requested JOIN the group \n",IP,PORT);

        // if this router is not part of a group
        if (isPartGroup == 0)
        {
            // send unsuccesful message
            write(sockfd, messageFAILED, sizeof(messageFAILED));
        }
        else
        {
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
                    fprintf(fptr, "Thread: %s:%s already in the group\n" ,IP, PORT);
                    break;
                }
            }

            if (flagUnique)
            {
                strncpy(neighbours[*curr_num_neigh].IP, IP, strlen(IP));
                strncpy(neighbours[*curr_num_neigh].PORT, PORT, strlen(PORT));

                *curr_num_neigh = *curr_num_neigh + 1;

                hasNeighbours = 1;
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

            fprintf(fptr,"Thread: Sending RP %s:%s to %s:%s\n", RP.IP, RP.PORT, IP, PORT);

            strcpy( _IP, RP.IP);
            strcpy( _PORT, RP.PORT);

	        read(sockfd, _message, sizeof(_message));
            fprintf(fptr,"Thread: Message from %s:%s [%s]\n",IP, PORT, _message);

            write(sockfd, _IP, sizeof(_IP));

	        read(sockfd, _message, sizeof(_message));
            fprintf(fptr,"Thread: Message from %s:%s [%s]\n",IP, PORT, _message);

            write(sockfd, _PORT, sizeof(_PORT));

        }

    }

    // a normal router thought this is a RP
    else if (strstr(buff, "JOIN") != NULL)
    {
        char messageERROR[] = "ERROR: CANNOT PROCESS REQUEST. THIS IS NOT A RP";
        // get requesting router IP and Port
        // ask for IP
        write(sockfd, messageERROR, sizeof(messageERROR));
    }
    

    // any other issue
    else
    {
        char messageERROR[] = "ERROR: CANNOT PROCESS REQUEST";
        // get requesting router IP and Port
        // ask for IP
        write(sockfd, messageERROR, sizeof(messageERROR));
    }
    
}

#endif 