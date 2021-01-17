
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <limits.h>

#include "utils.h"

/*********************************************************************
 *
 *  fibonacci function.
 *
 *   This is the target program to be profiled.
 *
 *********************************************************************/

#include <stdio.h>

int fib(int i)
{
    if (i <= 1) {
        return 1;
    }
    fib_logger(i-1, 1);
    return fib(i-1) + fib(i-2);
}

int main(int argc, char *argv[])
{
   int value;
   char *end;

   if (argc != 2) {
      fprintf(stderr, "usage: %s <value>\n", argv[0]);
      exit(1);
   }

   value = strtol(argv[1], &end, 10);

   if (((errno == ERANGE)
        && ((value == LONG_MAX) || (value == LONG_MIN)))
       || ((errno != 0) && (value == 0))) {
      perror("strtol");
      exit(1);
   }

   if (end == argv[1]) {
      fprintf(stderr, "error: %s is not an integer\n", argv[1]);
      exit(1);
   }

   if (*end != '\0') {
      fprintf(stderr, "error: junk at end of parameter: %s\n", end);
      exit(1);
   }

   value = fib(value);

   printf("%d\n", value);
   exit(0);
}



