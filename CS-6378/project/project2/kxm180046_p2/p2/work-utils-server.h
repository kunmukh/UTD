/* 
# File: work-utils-server.c
# Class: CS 6378                                    # Instructor: Dr. Ravi Prakash
# Assignment: Advance Operating System              # Date started: 02/06/2021
# Programmer: Kunal Mukherjee                       # Date completed:
*/

#ifndef WORK_UTILS_SERVER_H
#define  WORK_UTILS_SERVER_H

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
#include <bits/stdc++.h>

#include <sys/stat.h>
#include <string>
#include <vector>
#include <fstream>
#include <thread>

#include "init-utils.h"

using namespace std;

// number of threads
int n_threads = 0;

// global constants and variable needed for the communiation
#define MAX 256
#define SA struct sockaddr

char n_files[] = "3";
char file1[] = "t1.txt";
char file2[] = "t2.txt";
char file3[] = "t3.txt";

// flags
bool currFileOps[3] = {false, false, false}; // [t1.txt, t2.txt, t3.txt]


// request priority queue
vector <tuple <long, int, string>> requestQueue; // timestamp, sockfd, filename


// helper function to get the last line of a file
string getLastLine(string filename)
{
    ifstream fin;

    string line, buffer[1];
    
    string fname = "";
    fname.push_back(serverName);
    fname.append("/");
    fname.append(filename);
    
    fin.open(fname);

    while(getline(fin,line))
    {
        buffer[0] = line;
    }    

    return buffer[0];
}


// Function to take care of server wordload
void * serverWork(void *input)//int sockfd
{
    int sockfd = (long)input;

    // buffer to hold the initial messages
    char buffer[MAX];

    // clear out the buffer
    bzero(buffer, sizeof(buffer));

    // get the buffer that the client is sending
    while(read(sockfd, buffer, sizeof(buffer)))
    {
        // get the command
        char command[2];

        memcpy(command, &buffer[0], 1); 
        command[1] = '\0';

        printf("command: %s\n", command);

        // if the command is ENQUIRE
        // send the current list of files
        if (strncmp(command,"E",1)==0)
        {
            char enquireREPLY[MAX];

            // copy the files hosted in the client
            memcpy(&enquireREPLY[0], &n_files[0], 1);
            memcpy(&enquireREPLY[01], &file1[0], 10);
            memcpy(&enquireREPLY[11], &file2[0], 10);
            memcpy(&enquireREPLY[21], &file3[0], 10);

            // send the files hosted
            write(sockfd, enquireREPLY, sizeof(enquireREPLY)); 
            bzero(buffer, sizeof(buffer));
            
        }
        
        // if the current command is READ
        if (strncmp(command,"R",1)==0)
        {
            char readREPLY[MAX];

            char filename[MAX];
            memcpy(filename, &buffer[2], 10);

            // if none is READing/WRITEing the file
            if (!currFileOps[filename[1] - '0'])
            {
                // set read flag and filename
                currFileOps[filename[1] - '0'] = true;

                string line = getLastLine(filename);            

                cout << "READING:" << filename << ":" << line << endl;

                memcpy(&readREPLY, line.c_str(), line.size());

                // send the read success message
                write(sockfd, readREPLY, sizeof(readREPLY)); 
                bzero(buffer, sizeof(buffer));

                // reset flag and filename
                currFileOps[filename[1] - '0'] = false;
            }
        }

        // if the current command is WRITE
        if (strncmp(command,"W",1)==0)
        {
            // success message
            char writeREPLY[MAX] = "SUCCESS";

            // get the buffer
            int message_len = 29;
            char clientBUFFER[message_len+1];
            bzero(clientBUFFER, sizeof(clientBUFFER));
            memcpy(clientBUFFER, &buffer[strlen(command)+strlen(file1)+2], message_len);
            clientBUFFER[message_len] = '\0';

            // get the filename
            char filename[strlen(file1)];
            memcpy(filename, &buffer[2], strlen(file1));

            // if none is READing/WRITEing the file
            if (!currFileOps[filename[1] - '0'])
            {
                // message
                cout << "WRITING:" << filename << ":" << clientBUFFER << endl;

                // append the clientbuffer to the file
                ofstream outFile;

                string fname = "";
                fname.push_back(serverName);
                fname.append("/");
                fname.append(filename);

                outFile.open(fname, ios_base::app);
                outFile << clientBUFFER << endl;

                // send the write success message
                write(sockfd, writeREPLY, sizeof(writeREPLY)); 
                bzero(buffer, sizeof(buffer));

                // reset flag and filename
                currFileOps[filename[1] - '0'] = false;
            }
            
        }
    
    }

    // close the connection
	close(sockfd);

    // decrement the number of threads
	n_threads--;
    printf("Server work done...Num Threads:%d\n", n_threads);

}


#endif