# Assignment 0x1: Linking and Loading
# Kunal Mukherjee 

## Part 0 (0 point - warmup)

Basically run the make file and see what is the correct output. 

```
gcc -g -o part0  driver0.c
=== part0 ===
./part0
Standard memset: 0.022295
Int memset1: 1.498411
Int memset2: 1.548732
ASM memset: 0.021720
SSE memset: 0.104898
Failed at 2 (0)!
```

## Part 1: Building C source with Makefile (2pt)

For part 1, first we need to create the object files (ending with .o) using "gcc -g -c" command. Then, after the object files have been created using, run the "gcc -g -o" command to link the object files to create the executable. 

```
gcc -g -std=c99 -c driver1.c
gcc -g -c memsets.c
gcc -g -o part1 driver1.o memsets.o
=== part1 ===
./part1
Standard memset: 0.023734
Int memset1: 1.505411
Int memset2: 1.542609
ASM memset: 0.020248
SSE memset: 0.103083
Failed at 2 (0)!

```

## Part 2: Creating a static library (2pt)

For part 2, first we need to create the achieve file, libmemsets.a,  using "ar rs" command. Then, after the achieve is created use the same command "gcc -g -o" to link the achieve files to create the executable. 

```
ar rs libmemsets.a memsets.o
ar: creating archive libmemsets.a
gcc -g -o part2 driver1.o libmemsets.a
=== part2 ===
./part2
Standard memset: 0.022580
Int memset1: 1.511463
Int memset2: 1.550680
ASM memset: 0.020007
SSE memset: 0.105547
Failed at 2 (0)!
```

## Part 3: Creating a dynamic library (3pt)

For part 3, first we need to create the dynamic library, libmemsets.so,  using "gcc -shared" command. Then, after the dynamic file is created use the same "-g -o" to link the dynamic files to create the executable. In Linux system, you also have to specify the LD_LIBRARY_PATH=. , or else the system will not know where to find the dynamic library.

```
gcc -shared -o libmemsets.so memsets.o
gcc -g -o part3 driver1.o libmemsets.so
=== part3 ===
# LD_LIBRARY_PATH=. ./part3 # Linux
./part3
Standard memset: 0.023686
Int memset1: 1.508945
Int memset2: 1.558707
ASM memset: 0.020170
SSE memset: 0.104197
Failed at 2 (0)!

```

## Part 4: Dynamically load a library (3pt)

To dynamically load a library, I had to use the <dlfcn.h>. There, I used the dlopen to open the dynamic library. Then, I used the dlsym to symbolically link the function with the definition. And, use the definition to call the function with the arguments specified.

```
handle = dlopen ("./libmemsets.so", RTLD_LOCAL | RTLD_LAZY);

void (*memset1_)(void* str, char ch, size_t n);
memset1_ = dlsym(handle, "memset1");

(*memset1_)(mem, 61, sz);
```

For compilation, I had to use the "-ldl" flag to specify that a dynamic library needs to be loaded in runtime.

```
gcc -o part4 driver4.c -ldl
=== part4 ===
./part4
Standard memset: 0.024250
Int memset1: 1.497877
Int memset2: 1.554726
ASM memset: 0.020761
SSE memset: 0.103820
Failed at 2 (0)!
```

## Part 5: Library interposing with LD_PRELOAD (bonus 5pt)

First, I created a memsetinject.c file that contained a modified memset function that would be used to hijack the clib's memset function. 

```
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
```

Then, I create the dynamic library called memsetinject.so, using "gcc -shared" command.

```
#gcc -shared -fPIC -o memsetinject.so memsetinject.c # Linux
gcc -shared -fPIC -o memsetinject.so memsetinject.c # OS X
gcc -g -o part3exe driver1.o libmemsets.so
=== part5 ===
# LD_LIBRARY_PATH=. LD_PRELOAD=./memsetinject.so ./part3exe # Linux
LD_LIBRARY_PATH=. DYLD_INSERT_LIBRARIES=./memsetinject.so DYLD_FORCE_FLAT_NAMESPACE=1 ./part3exe # OS X
Kunal Memset change
Kunal Memset change
Standard memset: 0.021412
Int memset1: 1.507446
Int memset2: 1.675201
ASM memset: 0.021304
SSE memset: 0.104586
Failed at 2 (0)!
```

To hijack the clib's memset, it was very simple, I only had to specify the path DYLD_INSERT_LIBRARIES=./memsetinject.so . In that way 	I made sure, my modified dynamic library will be loaded first, and then use it to evaluate the memset function (originally intended for clib's symbol evaluation). Thus, change the specification fo the memset function as per my function's definition.