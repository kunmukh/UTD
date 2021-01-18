#ifndef __db_connector_utils_h__
#define __db_connector_utils_h__

#define BOOL char
#define TRUE  1
#define FALSE 0
void banner();
BOOL askYesOrNo();
BOOL isValid(char* user, char* pass);
int xorCipher(char* in, char* out);
int __xor_dbg(char* msg, char *in);

#endif
