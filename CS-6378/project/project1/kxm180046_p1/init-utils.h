/* 
# File: init-utils.c
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

#include <ctype.h>


// struct for neighbour router
// to contain IP and Port
struct neighbour{
	char IP[256];
	char PORT[256];
};


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
	// get the port 
	scanf("%d", &PORT);

	if ((PORT > 3000) && (PORT < 65000))
	{
		return PORT;
	}
	else
	{
		printf("Error in PORT reading...\n");
		exit(-1);
	}
	
}

// function to get IP and Port of servers
void getIPandPortserver(struct neighbour * servers, int n_server)
{
	// get the port and ip of the servers
	for (int i = 0; i < n_server; i++)
	{
		printf("Enter server IP Port(e.g. 192.168.1.1 8080):\n");
		scanf("%s %s", servers[i].IP, servers[i].PORT);
	}
}

/*// debug print
void printALL(struct neighbour * servers, int n_server, int PORT)
{
	printf("******DEBUG*****\n\n");
	// print all the info
	printf("PORT: %d\n", PORT);
	printf("Number of servers: %d\n", n_server);
	for (int i = 0; i < n_server; i++)
	{	
		printf("neigh: %d IP:%s PORT:%s\n",i, servers[i].IP, servers[i].PORT);
	}
}*/