#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "utils.h"

#define CMD_LEN  80
#define USER_LEN 16
#define PASS_LEN 16

#define HOST "10.176.150.50"

// defaults

typedef struct {
    char *user;
    char *pass;
} cred_t;

cred_t cred_default = {"cs6332", "mysecretpasswd"};

// redacting passwd input.
char pass_buf[16];

char *redactPass(char *pass) {
    // TODO: error handling needed for strlen, strncpy
    int len = strlen(pass);
    strncpy(pass_buf, pass, len);
    for (int i = 0; i < len - 2; i++) {
        pass_buf[i + 1] = '*';
    }

    return pass_buf;
}

int main(int argc, char *argv[]) {
    char cmd[80];
    char user[16];
    char pass[16];
    void *rc = 0;


    banner();

    printf("Input username: ");

    rc = fgets(user, USER_LEN, stdin);
    if (rc != NULL) {
        user[strlen(user) - 1] = '\0';
    } else {
        printf("Input error, exiting...\n");
        exit(1);
    }

    // TODO: need to redact input.
    char* temp =  getpass("Password:");
    if (temp != NULL) {
        pass[strlen(pass) - 1] = '\0';
        strncpy(pass, temp, 16);
    } else {
        printf("Input error, exiting...\n");
        exit(1);
    }

    if (!isValid(user, pass)) {
        fprintf(stderr, "Invalid credential input, using defaults\n");
        strncpy(user, cred_default.user, USER_LEN);
        strncpy(pass, cred_default.pass, PASS_LEN);
    }

    while (TRUE) {
        printf("can we proceed with username %s and password %s? ", user,
               redactPass(pass));
        if (!askYesOrNo()) {
            // No -- exiting ()
            fprintf(stderr, "Exiting ...\n");
            // exit(1);
            goto RET;
        }

        // Yes -- proceed with default credential.
        snprintf(cmd, CMD_LEN, "PGPASSWORD=%s psql -h %s -U %s", pass, HOST, user);
        system(cmd);
    }

    RET:
    return 0;
}
