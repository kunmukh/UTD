#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>

void* memset(void* mem, int value, size_t num) {
  char* m = mem;
  char v = value;
  while (num-- != 0)
    *(m + num) = v;
  printf("Kunal Memset change\n");
  return mem;
}