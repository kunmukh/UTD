/* 
# File: client.cpp
# Class: CS 6378                                    # Instructor: Dr. Ravi Prakash
# Assignment: Advance Operating System              # Date started: 03/14/2021
# Programmer: Kunal Mukherjee                       # Date completed:
*/

// add the libraries needed
#include <iostream>
#include <stdio.h>
#include <string>
#include <ctime>
#include <vector>

#include "init-utils.h"
#include "work-utils-client.h"

using namespace std;

// helper function to get the date
string getStringtoWrite(int clientID)
{
    time_t result = time(nullptr);
    string t = ctime(&result);
    return "<"+to_string(clientID)+","+t.substr(0, strlen(t.c_str())-1)+">";
}


int main(void)
{
	// print the current machine IP
	char * IP = getIP();

	// get the port number
	int PORT = getPort();

    struct server_args *self = (struct server_args*)malloc(sizeof(struct server_args));
    self->IP = IP;
    self->PORT = PORT;

    // get client ID
    int clientID;
    cout << "Enter clientID:" << endl;
    cin >> clientID;

	printf("Running as client\n");

	printf("Client IP:%s Port:%d\n", IP, PORT);

	// get the ip of the server neighbours
    printf("Enter Server information\n");
	getIPandPortNeighbour(serv_neighbours, n_serv_neigh);

	// debug 
	printALLNeighbour(serv_neighbours, n_serv_neigh, IP, PORT);

    // get the ip of the client neighbours
    printf("Enter Client information\n");
	getIPandPortNeighbour(client_neighbours, n_client_neigh);

	// debug 
	printALLNeighbour(client_neighbours, n_client_neigh, IP, PORT);

    // start the server
    pthread_t t0;
    pthread_create(&t0, NULL, startServer, (void *)self);

    // start the replyServer
    pthread_t t1;
    pthread_create(&t1, NULL, replySendFunction, (void *)self);

    // get READY
    int ready;
    cout << "PRESS [1] to begin simulation:" << endl;
    cin >> ready;


    // ENQUIRY(filenames[]) -> array of filename
    vector<string> files = clientWork('E', serv_neighbours, n_serv_neigh, client_neighbours, n_client_neigh, "", "");

    for (int i = 0; i < (int)files.size(); i++)
    {
        cout << "files:" << i << "/" << files.size() << ":" << files[i] << endl;
    }
    
    srand(time(0));
    int random_delay = 3;

    //todo: debug
    //int random_delay = 0;

    // trail runs
    for (int trial = 0; trial < 10; trial++)
    {
        int random_trail_read = rand() % 2;
        int random_num = rand() % 3;

        //todo: debug
        //int random_trail_read = 0;
        //int random_num = 0;

        if (random_trail_read)
        {
            // READ(filename) -> string
            cout << "READ file:" << files[0] << endl;
            cout << clientWork('R', serv_neighbours, n_serv_neigh, client_neighbours, n_client_neigh, files[random_num], "")[0] << endl;
        }
        else
        {
            // get the string to write to file    
            string line = getStringtoWrite(clientID);

            //WRITE(filename, writeString) -> "SUCCESS"
            cout << "WRITE file:" << files[random_num] <<":" << line << endl;
            cout << clientWork('W', serv_neighbours, n_serv_neigh,  client_neighbours, n_client_neigh, files[random_num], line)[0] << endl;            
        }

        // sleep for random_delay seconds
        sleep(random_delay);
    }

    while(1);

    return 0;
    
}