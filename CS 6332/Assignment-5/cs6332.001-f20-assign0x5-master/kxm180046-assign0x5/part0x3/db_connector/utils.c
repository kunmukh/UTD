#include <stdio.h>
#include <string.h>
#include "utils.h"

void banner() {
  printf("=======================================\n");
  printf("=            DB Connector             =\n");
  printf("=======================================\n");
}

BOOL askYesOrNo() {
    char buf[16];
    printf("(y / N) :");
    fgets(buf, 16, stdin);

    if (buf[0] == 'Y' || buf[0] == 'y') {
        return TRUE;
    }
    return FALSE;
}

BOOL isValid(char *user, char *pass) {
    return (strlen(user) > 4) && (strlen(pass) > 4);
}

static char xorKey = 0x07;  // bell -- non-printable character.

int __xor_dbg(char* msg, char *in) {
     printf("[%s] :",msg);
    int len = strlen(in);
    for (int i = 0; i < len; i++) {
        printf("\\%02X", in[i]);
    }
    printf("\\%02X", in[len]);
    printf("\n");
    return len;
}

int xorCipher(char *dst, char *src) {
    int len = strlen(src);
    for (int i = 0; i < len; i++) {
        //  Not a good cipher.
        dst[i] = src[i] ^ xorKey;
    }
    dst[len] = '\0';
    return len;
};
