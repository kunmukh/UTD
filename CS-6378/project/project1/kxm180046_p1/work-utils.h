/* 
# File: work-utils.c
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

#include <sys/stat.h>


// global constants and variable needed for the communiation
#define MAX 256
#define SA struct sockaddr

// var to file name
char dirname[11];

// Function designed the server work
void serverWork(int sockfd) 
{ 
    // buffer to hold the initial messages
    char buffer[MAX];

    // clear out the buffer
    bzero(buffer, sizeof(buffer));

    int clientCloseFlag = 0;

    // get the buffer that the client is sending
    while(read(sockfd, buffer, sizeof(buffer)))
    {
        // get the command
        char command[3];

        memcpy(command, &buffer[0], 2); 
        command[2] = '\0';

        printf("command: %s\n", command);

        // if the command is CReation of a dir or files
        if (strncmp(command,"CR",2)==0)
        {
            // var to selection is it dir or file
            char selection[2];

            memcpy(selection, &buffer[3], 1);
            selection[1] = '\0';

            printf("dir/file: %s\n", selection);

            // if the choice is Directory
            if (strncmp(selection,"D",1)==0)
            {               
            	// get the dir name from the client message
                memcpy(dirname, &buffer[5], 10);
                dirname[10] = '\0';

                printf("dirname: %s\n", dirname);

                // make the directory that the client wants to make
                strcat(dirname, "copy");

                // make the directory 
                int r = mkdir(dirname, 0777);

                // if creation was a success
                if (r == 0)
                {
                	char messageACK[] = "SUCCESS DIR MADE ACK";

                	// send the success DIR creation message to client
                	write(sockfd, messageACK, sizeof(messageACK)); 
                	bzero(buffer, sizeof(buffer));
                }
                else
                {
                	char messageACK[] = "FAILURE DIR MADE ACK";

                	// send the failure DIR creation message to client
                	write(sockfd, messageACK, sizeof(messageACK)); 
                	bzero(buffer, sizeof(buffer));
                }
            }
            // if the choice is File
            if (strncmp(selection,"F",1)==0)
            {
                // get the filename
                char filename[11];
                // need to create the file path
                char fullPath[11];

                bzero(fullPath, sizeof(fullPath));

                // get the filename
                memcpy(filename, &buffer[5], 10);
                filename[10] = '\0';

                // create the full file path
                strcat(fullPath, dirname);
                strcat(fullPath, "/");
                strcat(fullPath, filename);

                // make the file with the name
                FILE *fp;
                fp = fopen (fullPath, "w+");

                char messageACK[] = "SUCCESS FILE CREATED ACK";

                // send the ack message to the client about success file creation
                write(sockfd, messageACK, sizeof(messageACK)); 
                bzero(buffer, sizeof(buffer));

                // close the file
                fclose(fp);
            }
        }
        // get the command that we about to COpy of files
        if (strncmp(command,"CP",2)==0)
        {
            // variable to see that a file has to be created
            char selection[2];

            memcpy(selection, &buffer[3], 1);
            selection[1] = '\0';

            printf("dir/file: %s\n", selection);

            // get the copy a FIle
            if (strncmp(selection,"F",1)==0)
            {
                char messageACK[] = "SUCCESS FILE CONTENT REC ACK";

                // var to file name
                char filename[11];
                // var to store the file patj
                char fullPath[11];

                bzero(fullPath, sizeof(fullPath));

                memcpy(filename, &buffer[5], 10);
                filename[10] = '\0';

                strcat(fullPath, dirname);
                strcat(fullPath, "/");
                strcat(fullPath, filename);

                printf("filename: %s\n", fullPath);
                // open the file in writing mode
                FILE *fp;
                fp = fopen (fullPath, "w+");

                // variable to get the start command
                char startCommand[5];
                bzero(startCommand, sizeof(startCommand));

                memcpy(startCommand, &buffer[15], 5);

                // if the START command is send by the client
                // the means we need to keep reading and appending the file
                // and the client will sending the file content
                if (strncmp(startCommand,"START",5)==0)
                {
                	// send the ACK to singal start of FILE
                    bzero(buffer, sizeof(buffer));
                    write(sockfd, messageACK, sizeof(messageACK));

                    // keep on reading the buffer until the clients sends a EOF message
                    while(read(sockfd, buffer, sizeof(buffer))>1)
                    {
                        // need to check if EOF is send by the client
                        memcpy(startCommand, &buffer[15], 3);

                        // if EOF is send that means file is all send
                        // need to break out of it
                        if (strncmp(startCommand,"EOF",3)==0)
                        {
                            char messageSUCCESS[] = "SUCCESS FILE ALL REC ACK";

                            // send the successful copy of file ACK to client
                            write(sockfd, messageSUCCESS, sizeof(messageSUCCESS));
                            break;
                        }
                        else
                        {	
                        	// get the buffer and append it to the file
                            printf("buffer file recv:%s\n", buffer);
                            fprintf(fp, "%s", buffer);

                            bzero(buffer, sizeof(buffer));
                            // send the ACK message to the client
                            write(sockfd, messageACK, sizeof(messageACK));
                        }
                        
                    }
                }

                // close the file once we have received EOF flag
                fclose(fp);

                if (clientCloseFlag)
                {
                    // break out of the loop
                    break;
                }
            }
        }
        // client send this command that means all files in the DIR is done, 
        // need to close the connection and FINish the session
        if (strncmp(command,"FN",2)==0)
        {
        	// get the 
        	char EODCommand[5];
        	bzero(EODCommand, sizeof(EODCommand));

        	memcpy(EODCommand, &buffer[15], 5);

        	// if EOD is send, means end of directory so we close the connection
        	if (strncmp(EODCommand,"EOD",3)==0)
        	{
        	    char messageSUCCESS[] = "SUCCESS DIR ALL REC ACK";

        	    // send the ACK message of EOD to the client 
        	    write(sockfd, messageSUCCESS, sizeof(messageSUCCESS));
        	    clientCloseFlag = 1;
        	    break;
        	}
        }
 
    }   
}

// client work function
void clientWork(int sockfd) 
{ 
    // variable to store the buffer
    char buffer[MAX];

    // send the message to create a directory D1
    char messageCreateDir[] = "CR:D:D1";
    write(sockfd, messageCreateDir, sizeof(messageCreateDir)); 
    bzero(buffer, sizeof(buffer));

    // get the ACK response from the server
    read(sockfd, buffer, sizeof(buffer));    

    // get the ACK message that was sent from the server and print it
    char command[31];
    memcpy(command, &buffer[0], 30);
    command[30] = '\0';
    printf("%s\n", command);
    sleep(5);

    // send the message to create a file F1.txt in D1
    char messageCreateFile[] = "CR:F:F1.txt";
    write(sockfd, messageCreateFile, sizeof(messageCreateFile)); 
    bzero(buffer, sizeof(buffer));

    // get the response from the server
    read(sockfd, buffer, sizeof(buffer));

    // get the ACK message that was sent from the server and print it
    bzero(command, sizeof(command));
    memcpy(command, &buffer[0], 30);
    command[30] = '\0';
    printf("%s\n", command);
    sleep(5);

    // open the file that we want to be sent
    FILE * txFile;
    txFile = fopen("D1/F1.txt","r");

    // send the message to server that we will start
    //  sending the contents of the file F1.txt
    char messageCopyFile[] = "CP:F:F1.txt";
    char messageCopyStart[] = "START";
    char fullCommand[21];

    memcpy(&fullCommand[0], messageCopyFile, sizeof(messageCopyFile));
    memcpy(&fullCommand[15], messageCopyStart, sizeof(messageCopyStart));

    // send the message to the server 
    write(sockfd, fullCommand, sizeof(fullCommand)); 
    bzero(buffer, sizeof(buffer));
    char fileContent[240];
    char data;

    int filereadDone = 0;
    
    // once we recv the ACK from the server that it is ready
    // to start receiving the file,
    // we start sending the content
    while(read(sockfd, buffer, sizeof(buffer)) > 1)
    {
        
        bzero(command, sizeof(command));
        memcpy(command, &buffer[0], 30);
        command[30] = '\0';
        printf("%s\n", command);

        bzero(fileContent, sizeof(fileContent));

        // copy the files and put it in buffer
        for (int i = 0; i < 240; i++)
        {
        	// scan the file until EOF is received 
            if (fscanf(txFile, "%c", &data) != EOF)
            {
                fileContent[i] = data;
            }
            else
            {
            	// if EOF is received then break out
                filereadDone = 1;
                break;                
            }

        }

        // send the buffer contents that are the file contents
        printf("buffer file send:%s\n", fileContent);
        write(sockfd, fileContent, sizeof(fileContent));
        bzero(buffer, sizeof(buffer));


        // if the EOF is received 
        // we start sending the EOF flag
        if (filereadDone)
        {
        	// get the ACK from the server
            read(sockfd, buffer, sizeof(buffer));
            bzero(command, sizeof(command));
            memcpy(command, &buffer[0], 30);
            command[30] = '\0';
            printf("%s\n", command);

            // send the message to server that all contents have been sent
            char messagesFNFile[] = "FN:F:F1.txt";
            char messageEOF[] = "EOF";
            bzero(fullCommand, sizeof(fullCommand));

            memcpy(&fullCommand[0], messagesFNFile, sizeof(messagesFNFile));
            memcpy(&fullCommand[15], messageEOF, sizeof(messageEOF));

            // send the EOF flag to the server
            write(sockfd, fullCommand, sizeof(fullCommand)); 
            bzero(buffer, sizeof(buffer));

            // get the ACK from the server
            read(sockfd, buffer, sizeof(buffer));    

            char command[31];
            memcpy(command, &buffer[0], 30);
            command[30] = '\0';
            printf("%s\n", command);

            break;
        }

    }

    // close the text file that was opened
    fclose(txFile);
    sleep(10);

    //--------------------
    // exactly whats happening before

    // send the message to create a file F2.txt in D1
    char messageCreateFile2[] = "CR:F:F2.txt";
    write(sockfd, messageCreateFile2, sizeof(messageCreateFile2)); 
    bzero(buffer, sizeof(buffer));

    // get the ACK response from the server
    read(sockfd, buffer, sizeof(buffer));

    // get the ACK from the server
    bzero(command, sizeof(command));
    memcpy(command, &buffer[0], 30);
    command[30] = '\0';
    printf("%s\n", command);
    sleep(5);

    // open the file F2.txt to read and send it 
    txFile = fopen("D1/F2.txt","r");

    // send the message to server that we will start
    //  sending the contents of the file F2.txt
    char messageCopyFile2[] = "CP:F:F2.txt";

    bzero(fullCommand, sizeof(fullCommand));

    memcpy(&fullCommand[0], messageCopyFile2, sizeof(messageCopyFile2));
    memcpy(&fullCommand[15], messageCopyStart, sizeof(messageCopyStart));

    // send the message to that we will start 
    // to send the contents of file F2.txt in D1
    write(sockfd, fullCommand, sizeof(fullCommand)); 
    bzero(buffer, sizeof(buffer));

    filereadDone = 0;
    
    // once we recv the ACK from the server that it is ready
    // to start receiving the file,
    // we start sending the content
    while(read(sockfd, buffer, sizeof(buffer)) > 1)
    {
        
        bzero(command, sizeof(command));
        memcpy(command, &buffer[0], 30);
        command[30] = '\0';
        printf("%s\n", command);

        bzero(fileContent, sizeof(fileContent));

        // copy the files and put it in buffer
        for (int i = 0; i < 240; i++)
        {
            // scan the file until EOF is received
            if (fscanf(txFile, "%c", &data) != EOF)
            {
                fileContent[i] = data;
            }
            else
            {
                // if EOF is received then break out
                filereadDone = 1;
                break;                
            }

        }

        // send the buffer contents that are the file contents
        printf("buffer file send:%s\n", fileContent);
        write(sockfd, fileContent, sizeof(fileContent));
        bzero(buffer, sizeof(buffer));

        // if the EOF is done
        if (filereadDone)
        {
            // get the ACK from the server
            read(sockfd, buffer, sizeof(buffer));
            bzero(command, sizeof(command));
            memcpy(command, &buffer[0], 30);
            command[30] = '\0';
            printf("%s\n", command);

            // send the message to server that all contents have been sent
            char messageFNfile[] = "FN:F:F2.txt";
            char messageEOF[] = "EOF";
            bzero(fullCommand, sizeof(fullCommand));

            memcpy(&fullCommand[0], messageFNfile, sizeof(messageFNfile));
            memcpy(&fullCommand[15], messageEOF, sizeof(messageEOF));

            // send the message that all content has been send
            // send the EOF flag
            write(sockfd, fullCommand, sizeof(fullCommand)); 
            bzero(buffer, sizeof(buffer));

            // get the ACK from the server
            read(sockfd, buffer, sizeof(buffer));    

            char command[31];
            memcpy(command, &buffer[0], 30);
            command[30] = '\0';
            printf("%s\n", command);

            break;
        }

    }

    fclose(txFile);

    //--------------

    // send the message that end of transmission
    // sending the EOD flag to the server
    char messageCopyEND[] = "EOD";
    char messageCopyFileEND[] = "FN:F:F2.txt";

    bzero(fullCommand, sizeof(fullCommand));

    memcpy(&fullCommand[0], messageCopyFileEND, sizeof(messageCopyFileEND));
    memcpy(&fullCommand[15], messageCopyEND, sizeof(messageCopyEND));

    // send the message to the server 
    // and we will close the connection
    write(sockfd, fullCommand, sizeof(fullCommand)); 
    bzero(buffer, sizeof(buffer));

    // get the reply from the server and close the connections
    read(sockfd, buffer, sizeof(buffer));    
	bzero(command, sizeof(command));
    memcpy(command, &buffer[0], 30);
    command[30] = '\0';
    printf("%s\n", command);

} 