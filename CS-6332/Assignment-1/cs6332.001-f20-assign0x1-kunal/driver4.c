#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <dlfcn.h>

void check(char* mem, int sz, int val) {
  for (int i = 0; i < sz; i++) {
    if (*(mem + i) != val) {
      printf("Failed at %i (%x)!\n", i, *(mem + i));
      break;
      }
  }
}

int main(int argc, char** argv) {

  //------
  // kunal edit
  void *handle;
  handle = dlopen ("./libmemsets.so", RTLD_LOCAL | RTLD_LAZY);

  void (*memset1_)(void* str, char ch, size_t n);
  memset1_ = dlsym(handle, "memset1");

  void (*memset2_)(void* str, char ch, size_t n);
  memset2_ = dlsym(handle, "memset2");

  void (*memset_asm_)(void* ptr, int value, size_t num);
  memset_asm_ = dlsym(handle, "memset_asm");

  void (*memset_sse_)(void* mem, int value, size_t num);
  memset_sse_ = dlsym(handle, "memset_sse");
  //------
  
  

  unsigned int i, e = 1024, sz = 1024 * 1024;
  clock_t start, stop;
  char* mem = (char*) malloc(sz);

  start = clock();
  for (i = 0; i < e; i++) {
    memset(mem, 61, sz);
  }
  stop = clock();
  printf("Standard memset: %f\n", ((double) stop - start) / CLOCKS_PER_SEC);
  check(mem, sz, 61);

  memset(mem, 0, sz);

  start = clock();
  for (i = 0; i < e; i++) {
    //------
    // kunal edit
    (*memset1_)(mem, 61, sz);
    //------
  }
  stop = clock();
  printf("Int memset1: %f\n", ((double) stop - start) / CLOCKS_PER_SEC);
  check(mem, sz, 61);
  memset(mem, 0, sz);


  start = clock();
  for (i = 0; i < e; i++) {
    //------
    // kunal edit
    (*memset2_)(mem, 61, sz);
    //------
  }
  stop = clock();
  printf("Int memset2: %f\n", ((double) stop - start) / CLOCKS_PER_SEC);
  check(mem, sz, 61);
 

  memset(mem, 0, sz);
  
  start = clock();
  for (i = 0; i < e; i++) {
    //------
    // kunal edit
    (*memset_asm_)(mem, 61, sz);
    //------
  }
  stop = clock();

  printf("ASM memset: %f\n", ((double) stop - start) / CLOCKS_PER_SEC);
  check(mem, sz, 61);

  memset(mem, 0, sz);
  
  start = clock();
  for (i = 0; i < e; i++) {
    //------
    // kunal edit
    (*memset_sse_)(mem, 61, sz);
    //------
  }
  stop = clock();

  printf("SSE memset: %f\n", ((double) stop - start) / CLOCKS_PER_SEC);
  check(mem, sz, 61);

  //------
  // kunal edit
  dlclose(handle);
  //------

  return 0;
}
