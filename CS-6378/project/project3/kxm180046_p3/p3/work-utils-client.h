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

// number of threads
int n_threads = 0;

// lamport clock
int l_clock = 0;

// client level locking
int current_work[3] = {0,0,0};
int request_file[3] = {0,0,0};

// release variable
int release = 1;

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

// Maekawa's variable
tuple <string, int> currRequest; // ip, l_clock
int recvFailed = 0; 

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

    // send the message to REQUEST to enter CS
    string messageRequest = "R:";

    // increment the lamport clock
    l_clock++;
    char l_clock_c = l_clock;
    
    //copy the request first
    memcpy(&buffer[0], messageRequest.c_str(), messageRequest.size());
    memcpy(&buffer[5], &l_clock_c, sizeof(l_clock_c));
    memcpy(&buffer[10], filename.c_str(), filename.size());

    cout << "client REQUEST:" << c_neighbour.IP << ":" << filename << endl;

    // write the request string
    write(sockfd, buffer, sizeof(buffer)); 
    bzero(buffer, sizeof(buffer));

    // get the ACK response from the server
    read(sockfd, buffer, sizeof(buffer));

    // Maekawa's failed
    // get the command
    char command[2];

    memcpy(command, &buffer[0], 1); 
    command[1] = '\0';

    printf("command: %s\n", command);

    // if the command is FAILED
    if (strncmp(command,"F",1)==0)
    {
        // Maekawa's failed
        cout << "quorum FAILED" << c_neighbour.IP << ":" << filename << endl;
        recvFailed = 1;
    }

    // get the ACK message that was sent from the server and print it
    char reply[28];
    bzero(reply, sizeof(reply));
    memcpy(reply, &buffer[0], 7);
    
    cout << "quorum REPLIED:" << c_neighbour.IP << ":" << filename << ":" << reply << endl;

    // close the socket 
    close(sockfd);

    free(input);

}


// function that gets the permission 
// from the other clients to be able to enter the CS
// Maekawa's algorithm
int getPermission(string filename, struct neighbour * cli_neighbours, int n_cli_neighbours)
{
    // Maekawa's Algorithm
    // init receive failed to 0
    recvFailed = 0;

    pthread_t t[n_cli_neighbours];
    bool threadFlag[2] = {false, false};

    // ask the permission to the clients
    // once all of them reply then only return
    for (int client_num = 0; client_num < n_cli_neighbours; client_num++) 
    {        
        struct clientPermissionWorkargs *args = (struct clientPermissionWorkargs *)malloc(sizeof(struct clientPermissionWorkargs));

        args->client = cli_neighbours[client_num];
        strcpy (args->filename, filename.c_str());

        // create a thread to handle this request
		pthread_create(&t[client_num], NULL, clientPermissionWork, (void *)args);

        threadFlag[client_num] = true;
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


// send release message
int sendRelease(struct neighbour * cli_neighbours, int n_cli_neighbours)
{
    // send the release to all the quorum
    for (int client_num = 0; client_num < n_cli_neighbours; client_num++) 
    {
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
        servaddr.sin_addr.s_addr = inet_addr(cli_neighbours[client_num].IP); 
        servaddr.sin_port = htons(atoi(cli_neighbours[client_num].PORT)); 
            
        // connect the client socket to server socket 
        if (connect(sockfd, (SA*)&servaddr, sizeof(servaddr)) != 0) 
        { 
            printf("connection with the client failed : %s %s\n",cli_neighbours[client_num].IP, cli_neighbours[client_num].PORT); 
            exit(0); 
        } 
        else
        {
            printf("Connected to the client: %s %s\n", cli_neighbours[client_num].IP, cli_neighbours[client_num].PORT);
        }
            
        // Function for get the client work done 
        // variable to store the buffer
        char buffer[MAX];

        // send the message to RELEASE to enter CS
        string messageRelease = "E:";

        memcpy(&buffer[0], messageRelease.c_str(), messageRelease.size());

        // increment the lamport clock
        l_clock++;
        char l_clock_c = l_clock;

        cout << "client RELEASE:" << cli_neighbours[client_num].IP << endl;

        // write the RELEASE string
        write(sockfd, buffer, sizeof(buffer));

        // close the socket 
        close(sockfd);

    }
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

            // send release meaage
            sendRelease(c_neighbours, n_c_neighbours);

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

            // send release
            sendRelease(c_neighbours, n_c_neighbours);

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


// helper function to send message
string sendMessage(string message, string ip)
{
    string reply = "";

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
    servaddr.sin_addr.s_addr = inet_addr(ip.c_str()); 
    servaddr.sin_port = htons(atoi("4040")); 
            
    // connect the client socket to server socket 
    if (connect(sockfd, (SA*)&servaddr, sizeof(servaddr)) != 0) 
    { 
        printf("connection with the client failed : %s %s\n",ip.c_str(), "4040"); 
        exit(0); 
    } 
    else
    {
        printf("Connected to the client: %s %s\n",ip.c_str(), "4040");
    }
            
    // Function for get the client work done 
    // variable to store the buffer
    char buffer[MAX];

    // send the message
    string messageRelease = message;

    memcpy(&buffer[0], messageRelease.c_str(), messageRelease.size());

    // increment the lamport clock
    l_clock++;
    char l_clock_c = l_clock;

    // write the RELEASE string
    write(sockfd, buffer, sizeof(buffer));

    // close the socket 
    close(sockfd);

    return reply;
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

            // Maekawa's Algorithm
            // site Pj for a request that higher priority than the request it is
            // currenly granted
            if (l_clock_c < get<1>(currRequest))
            {
                // sending an INQUIRE message to the current process
                cout << "Got a process with higher priority";
                cout << "sending INQUIRE:" << get<0>(currRequest) << endl;

                // send INQUIRE and see if we get YIELD reply
                string reply = sendMessage("INQUIRE", get<0>(currRequest));

                // YIELD message
                // send the new grant message and place the current process in the queue
                if (strncmp(reply.c_str(),"Y",1)==0)
                {
                    // send the grant message
                    cout << "Sending GRANT message" <<  ":" << get<0>(currRequest) << endl;

                    // send the grant hosted
                    sendMessage("GRANT", get<0>(currRequest));

                    release = 0;
                }
               
            } else{
                // sending failed message as Pj has lower priority as Pk
                cout << "sending FAILED:" << get<0>(currRequest) << endl;

                sendMessage("FAILED", get<0>(currRequest));
            }

            cout << "old_lamport:"<< l_clock << " new_lamport:"<< MAX_FUNC(l_clock+1,l_clock_c+1)<< " file:" << filename << endl;
            l_clock = MAX_FUNC(l_clock+1, l_clock_c+1);

            // do something
            requestQueue.push_back(tuple<int, int, string>(connfd, l_clock, string(filename)));
            cout << "REQUEST:" << connfd << ":" << l_clock << ":" << filename << endl;

            // sort the requestQueue
            sort(requestQueue.begin(), requestQueue.end(), sortbyclock);

        }   
        // RELEASE message
        if (strncmp(command,"E",1)==0)
        {
            release = 1;
            cout << "RELEASE message received:" << connfd << endl;
        }
        if (strncmp(command,"I",1)==0)
        {
            if (recvFailed)
            {
                // send the grant message
                cout << "Sending YIELD message" <<  ":" << get<0>(currRequest) << endl;

                // send the grant hosted
                sendMessage("YIELD", get<0>(currRequest));
            }
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
// Maekawa's Algorithm
void * replySendFunction(void *input)
{
    while (1)
    {
        // if the queue is not empty
        if (requestQueue.size() > 0 && release)
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

            cout << "REPLYING:" << conn << ":" << clientIP << ":" << r_time << ":" << need_filename << endl;

            // Maekawa's Algo
            //store the current request that is being worked
            currRequest = make_tuple(string(clientIP), r_time);            

            // if i am not in the cs and
            // i am not requesting 
            // then reply
            if ((!current_work[((int)need_filename[1]) - ((int) '0')]) &&
                (!request_file[((int)need_filename[1]) - ((int) '0')]))
            {
                char REPLY[MAX] = "GRANTED";

                cout << "Sending GRANT message" <<  ":" << clientIP << endl;

                // send the files hosted
                write(conn, REPLY, sizeof(REPLY));

                release = 0;

                close(conn);

                requestQueue.erase(requestQueue.begin());

            }
            
            // if i am not in the cs but
            // i am requesting
            // need to check the time stamp
            if ((!current_work[((int)need_filename[1]) - ((int) '0')]) &&
                (request_file[((int)need_filename[1]) - ((int) '0')]))
            {
                // if the Pj request has lower time stamp then we reply
                if (r_time <=  request_file[((int)need_filename[1]) - ((int) '0')])
                {
                    char REPLY[MAX] = "GRANTED";

                    // send the files hosted
                    write(conn, REPLY, sizeof(REPLY));

                    close(conn);

                    requestQueue.erase(requestQueue.begin());
                }
            }
        }
        // sleep for some seconds
        sleep(2);
    }
}


#endif