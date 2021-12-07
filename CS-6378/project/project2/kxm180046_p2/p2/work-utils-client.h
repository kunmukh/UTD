/* 
# File: work-utils-client.c
# Class: CS 6378                                    # Instructor: Dr. Ravi Prakash
# Assignment: Advance Operating System              # Date started: 02/06/2021
# Programmer: Kunal Mukherjee                       # Date completed:
*/

#ifndef WORK_UTILS_CLIENT_H
#define  WORK_UTILS_CLIENT_H

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
#include <time.h>

#include <sys/stat.h>
#include <string>
#include <vector>
#include <fstream>
#include <thread>
#include <bits/stdc++.h>

#include "init-utils.h"

using namespace std;

// number of neighbours
// todo: debug change
int n_serv_neigh = 3;
struct neighbour serv_neighbours[3];

int n_client_neigh = 2;
struct neighbour client_neighbours[2];

// roucairol-Carvalho
int roucairol[2] = {0,0};

// number of threads
int n_threads = 0;

// lamport clock
int l_clock = 0;

// client level locking
int current_work[3] = {0,0,0};
int request_file[3] = {0,0,0};

// define the clientPermissionWorkargs
struct clientPermissionWorkargs {
    neighbour client;
    char filename[7]; //"t1.txt"
};

struct server_args{
    char * IP;
    int PORT;
};

// global constants and variable needed for the communiation
#define MAX 256
#define SA struct sockaddr

// request priority queue
vector <tuple <int, int, string>> requestQueue; // sockfd, l_clock, filename


// function that client uses to enquire from server
void clientENQUIRE(int sockfd, vector<string> &results)
{
    // variable to store the buffer
    char buffer[MAX];

    // send the message to read the lastline of the filename
    string messageCreateDir = "E:";
    write(sockfd, messageCreateDir.c_str(), sizeof(messageCreateDir.c_str())); 
    bzero(buffer, sizeof(buffer));

    // get the ACK response from the server
    read(sockfd, buffer, sizeof(buffer));    

    // get the ACK message that was sent from the server and print it
    char line[MAX];
    memcpy(line, &buffer[0], MAX);

    int num_files = line[0] - '0';

    for (int i = 0; i < num_files; i++)
    {
        char fileName[10];
        memcpy(fileName, &buffer[(i * 10) + 1], 10);
        results.push_back(fileName);
    }

}


// function that client uses to read from server
string clientREAD(int sockfd, string filename)
{
    // variable to store the buffer
    char buffer[MAX];

    // send the message to read the lastline of the filename
    string messageCreateDir = "R:"+filename;
    write(sockfd, messageCreateDir.c_str(), sizeof(messageCreateDir.c_str())); 
    bzero(buffer, sizeof(buffer));

    // get the ACK response from the server
    read(sockfd, buffer, sizeof(buffer));    

    // get the ACK message that was sent from the server and print it
    char line[MAX];
    memcpy(line, &buffer[0], MAX-1);
    line[MAX-1] = '\0';
    
    return line;
}


// function that client uses to write to server
string clientWRITE(int sockfd, string filename, string line)
{
   // variable to store the buffer
    char buffer[MAX];

    // send the message to read the lastline of the filename
    string messageCreateDir = "W:"+filename+":"+line;
    write(sockfd, messageCreateDir.c_str(), messageCreateDir.size()); 
    bzero(buffer, sizeof(buffer));

    // get the ACK response from the server
    read(sockfd, buffer, sizeof(buffer));    

    // get the ACK message that was sent from the server and print it
    char status[28];
    bzero(status, sizeof(status));
    memcpy(status, &buffer[0], 28);
    
    return status;
}


// Function to take get permission fo each client
void * clientPermissionWork(void *input)
{
    neighbour c_neighbour = ((struct clientPermissionWorkargs*) input)->client; 
    string filename = string(((struct clientPermissionWorkargs*) input)->filename);
    
    // create a connection
    int sockfd; 
	struct sockaddr_in servaddr;

    // socket create and verification 
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
    servaddr.sin_addr.s_addr = inet_addr(c_neighbour.IP); 
    servaddr.sin_port = htons(atoi(c_neighbour.PORT)); 
        
    // connect the client socket to server socket 
    if (connect(sockfd, (SA*)&servaddr, sizeof(servaddr)) != 0) 
    { 
        printf("connection with the client failed : %s %s\n",c_neighbour.IP, c_neighbour.PORT); 
        exit(0); 
    } 
    else
    {
        printf("Connected to the client: %s %s\n", c_neighbour.IP, c_neighbour.PORT);
    }
        
    // Function for get the client work done 
    // variable to store the buffer
    char buffer[MAX];

    // send the message to read the lastline of the filename
    string messageRequest = "R:";

    // increment the lamport clock
    l_clock++;
    char l_clock_c = l_clock;
    
    //copy the request first
    memcpy(&buffer[0], messageRequest.c_str(), messageRequest.size());
    memcpy(&buffer[5], &l_clock_c, sizeof(l_clock_c));
    memcpy(&buffer[10], filename.c_str(), filename.size());

    // write the request string
    write(sockfd, buffer, sizeof(buffer)); 
    bzero(buffer, sizeof(buffer));

    // get the ACK response from the server
    read(sockfd, buffer, sizeof(buffer));    

    // get the ACK message that was sent from the server and print it
    char reply[28];
    bzero(reply, sizeof(reply));
    memcpy(reply, &buffer[0], 7);
    
    cout << "serverREQUEST:" << c_neighbour.IP << ":" << filename << ":" << reply << endl;

    // close the socket 
    close(sockfd);

    free(input);

    // once i received reply from j
    for (int j = 0 ; j < n_client_neigh; j++)
    {
	    if (strcmp(client_neighbours[j].IP, c_neighbour.IP) == 0)
        {
            // set the permission
            roucairol[j] = 1;
        }
    }
}


// function that gets the permission 
// from the other clients to be able to enter the CS
// Ricart-Agarwal algorithm
int getPermission(string filename, struct neighbour * cli_neighbours, int n_cli_neighbours)
{   

    pthread_t t[n_cli_neighbours];
    bool threadFlag[4] = {false, false, false, false};

    // ask the permission to the clients
    // once all of them reply then only return
    for (int client_num = 0; client_num < n_cli_neighbours; client_num++) 
    {
        // if i dont have the permission then only ask
        if (!roucairol[client_num])
        {

	        struct clientPermissionWorkargs *args = (struct clientPermissionWorkargs *)malloc(sizeof(struct clientPermissionWorkargs));

            args->client = cli_neighbours[client_num];
            strcpy (args->filename, filename.c_str());

            // create a thread to handle this request
		    pthread_create(&t[client_num], NULL, clientPermissionWork, (void *)args);

            threadFlag[client_num] = true;
        }        

    }

    // wait for all the threads to join
    for (int client_num = 0; client_num < n_cli_neighbours; client_num++) 
    {
		if (threadFlag[client_num])
        {
            pthread_join(t[client_num], NULL);
        }
        
    }

    cout << "Got permission from clients. Entering CS:" << filename << endl;
    return true;
    
}


// main driver function for the client workload
vector<string> clientWork(int choice, 
                struct neighbour * s_neighbours, 
                int n_s_neighbours,
                struct neighbour * c_neighbours, 
                int n_c_neighbours,
                string filename,
                string line)
{
    vector<string> results;

    // create a connection
    int sockfd; 
	struct sockaddr_in servaddr;

    // choose a random server to enquire/read
    // todo: change
    srand(time(0));
    int random_num = rand() % 3;
    
    // debug random
    //int random_num = 0;

    switch (choice)
    {
        case 'E': // Enquiry         
		{ 
            // socket create and verification 
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
            servaddr.sin_addr.s_addr = inet_addr(s_neighbours[random_num].IP); 
            servaddr.sin_port = htons(atoi(s_neighbours[random_num].PORT)); 
			  
            // connect the client socket to server socket 
            if (connect(sockfd, (SA*)&servaddr, sizeof(servaddr)) != 0) 
            { 
                printf("connection with the server failed...\n"); 
                exit(0); 
            } 
            else
            {
                printf("Connected to the server: %s %s\n", s_neighbours[random_num].IP, s_neighbours[random_num].PORT);
            }
			  
            // Function for get the client work done 
            clientENQUIRE(sockfd, results); 
                    
            // close the socket 
            close(sockfd);

            break;
        }
        case 'R': // Read
        {
            // set the file that you want to request
            l_clock++;
            request_file[((int)filename[1]) - ((int) '0')] = l_clock;

            // get permission to enter the CS from the client
            int status = getPermission(filename, c_neighbours, n_c_neighbours);

            // update the current work
            current_work[((int)filename[1]) - ((int) '0')] = 1;
            
            // socket create and verification 
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
            servaddr.sin_addr.s_addr = inet_addr(s_neighbours[random_num].IP); 
            servaddr.sin_port = htons(atoi(s_neighbours[random_num].PORT)); 
			  
            // connect the client socket to server socket 
            if (connect(sockfd, (SA*)&servaddr, sizeof(servaddr)) != 0) 
            { 
                printf("connection with the server failed: %s %s\n", s_neighbours[random_num].IP, s_neighbours[random_num].PORT);
                exit(0); 
            } 
            else
            {
                printf("Connected to the server: %s %s\n", s_neighbours[random_num].IP, s_neighbours[random_num].PORT);
            }
			  
            // Function for get the client work done 
            string r_line = clientREAD(sockfd, filename); 
            results.push_back(r_line);

            // close the socket 
            close(sockfd);

            // update the current work
            current_work[((int)filename[1]) - ((int) '0')] = 0;

            // unset the file that you want to request
            request_file[((int)filename[1]) - ((int) '0')] = 0;

            break;
        }
        case 'W': // Write
        {
            // set the file that you want to request
            l_clock++;
            request_file[((int)filename[1]) - ((int) '0')] = l_clock;

            // get permission to enter the CS
            int status = getPermission(filename, c_neighbours, n_c_neighbours);

            // update the current work
            current_work[((int)filename[1]) - ((int) '0')] = 1;

            for (int server_num = 0; server_num < n_s_neighbours; server_num++) 
            {
                // socket create and verification 
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
                servaddr.sin_addr.s_addr = inet_addr(s_neighbours[server_num].IP); 
                servaddr.sin_port = htons(atoi(s_neighbours[server_num].PORT)); 
                    
                // connect the client socket to server socket 
                if (connect(sockfd, (SA*)&servaddr, sizeof(servaddr)) != 0) 
                { 
                    printf("connection with the server failed : %s %s\n",s_neighbours[server_num].IP, s_neighbours[server_num].PORT); 
                    exit(0); 
                } 
                else
                {
                    printf("Connected to the server: %s %s\n", s_neighbours[server_num].IP, s_neighbours[server_num].PORT);
                }
                    
                // Function for get the client work done 
                string ack_Server = clientWRITE(sockfd, filename, line); 
                results.push_back(ack_Server);

                // close the socket 
                close(sockfd);

                // update the current work
                current_work[((int)filename[1]) - ((int) '0')] = 0;

                // unset the file that you want to request
                request_file[((int)filename[1]) - ((int) '0')] = 0;
            }            

            break;
        }
        
    }

    return results;

}


// helper funtion for sorting the queue
bool sortbyclock(const tuple<int, int, string>& a, const tuple<int, int, string>& b)
{
    return (get<1>(a) < get<1>(b)); 
}


// Function to take care of server wordload
void * serverWork_client(void *input)
{
    int connfd = (long)input;

    // buffer to hold the initial messages
    char buffer[MAX];

    // clear out the buffer
    bzero(buffer, sizeof(buffer));

    // get the buffer that the client is sending
    while(read(connfd, buffer, sizeof(buffer)))
    {
        // get the command
        char command[2];

        memcpy(command, &buffer[0], 1); 
        command[1] = '\0';

        printf("command: %s\n", command);

        // if the command is REQUEST
        // send the current list of files
        if (strncmp(command,"R",1)==0)
        {
            // get the current clock value
            int l_clock_c = buffer[5];

            // get the filename
            char filename[7];
            memcpy(filename, &buffer[10], 6); 
            filename[6] = '\0';

            cout << "old_lamport:"<< l_clock << " new_lamport:"<< MAX_FUNC(l_clock+1,l_clock_c+1)<< " file:" << filename << endl;
            l_clock = MAX_FUNC(l_clock+1, l_clock_c+1);

            // do something
            requestQueue.push_back(tuple<int, int, string>(connfd, l_clock, string(filename)));
            cout << "connfd:" << connfd << ":" << l_clock << ":" << filename << endl;

            // sort the requestQueue
            sort(requestQueue.begin(), requestQueue.end(), sortbyclock);

        }
    
    }

}


// start the server
void  * startServer(void *input)
{
    char * IP = ((struct server_args*) input)->IP;
    int PORT = ((struct server_args*) input)->PORT;

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
		pthread_create(&t, NULL, serverWork_client, (void *)connfd);

		printf("Server work for client create...\n");
	}		  
		
	// close the socket
	close(sockfd);

}


// function that checks in few minutes 
// and sends out defer reply
// Richart-Agarwal Algorithm
void * replySendFunction(void *input)
{
    while (1)
    {
        // if the queue is not empty
        if (requestQueue.size() > 0)
        {
            int conn = get<0>(requestQueue[0]);
            int r_time = get<1>(requestQueue[0]);
            string need_filename = get<2>(requestQueue[0]);
            
            // get the ip and port
            struct sockaddr_in my_addr;
            char clientIP[256];
            bzero(&my_addr, sizeof(my_addr));
            socklen_t len = sizeof(my_addr);
            getpeername(conn, (struct sockaddr *) &my_addr, &len);
            inet_ntop(AF_INET, &(my_addr.sin_addr), clientIP, sizeof(clientIP));

            cout << "connfd:" << conn << ":" << clientIP << ":" << r_time << ":" << need_filename << endl;
            

            // if i am not in the cs and
            // i am not requesting 
            // then reply
            if ((!current_work[((int)need_filename[1]) - ((int) '0')]) &&
                (!request_file[((int)need_filename[1]) - ((int) '0')]))
            {
                char REPLY[MAX] = "GRANTED";

                // send the files hosted
                write(conn, REPLY, sizeof(REPLY));

                // once i received reply from j
                for (int j = 0 ; j < n_client_neigh; j++)
                {
                    if (strcmp(client_neighbours[j].IP, clientIP) == 0)
                    {
                        // set the permission
                        roucairol[j] = 0;
                    }
                }

                close(conn);

                requestQueue.erase(requestQueue.begin());

            }
            
            // if i am not in the cs but
            // i am requesting
            // neec to check the time stamp
            if ((!current_work[((int)need_filename[1]) - ((int) '0')]) &&
                (request_file[((int)need_filename[1]) - ((int) '0')]))
            {
                // if the Pj request has lower time stamp then we reply
                if (r_time <=  request_file[((int)need_filename[1]) - ((int) '0')])
                {
                    char REPLY[MAX] = "GRANTED";

                    // send the files hosted
                    write(conn, REPLY, sizeof(REPLY));

                    // once i received reply from j
                    for (int j = 0 ; j < n_client_neigh; j++)
                    {
                        if (strcmp(client_neighbours[j].IP, clientIP) == 0)
                        {
                            // set the permission
                            roucairol[j] = 0;
                        }
                    }

                    close(conn);

                    requestQueue.erase(requestQueue.begin());
                }
            }
        }
        /*else
        {
            //printf("Request Queue is empty\n");
            //fflush(stdout);
        }*/
        // sleep for some seconds
        sleep(2);
    }
}

#endif
