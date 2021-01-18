#include <stdio.h>
#include <stdlib.h>

int fib_logger(int val, int isCall) {
    char *fmt;

    if (!atoi(getenv("FIB_LOGGER"))) {
        return -1;
    }

    if (isCall) {
        fmt = "call fib(%d)\n";
    } else {
        fmt = "fib() returns %d\n";
    }
    fprintf(stderr, fmt, val);
    return val;
}