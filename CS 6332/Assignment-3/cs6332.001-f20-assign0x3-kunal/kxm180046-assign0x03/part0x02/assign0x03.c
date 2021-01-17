#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <limits.h>

#include "macros.h"
#include "ia32_context.h"

/* addresses of asm callout glue code */

extern void* retCallout;

/*********************************************************************
 *
 *  callout handler
 *
 *   These get called by asm glue routines.
 *
 *********************************************************************/

void
handleRetCallout(SaveRegs regs)
{
   // TODO: add your own routine.
   printf("inside return callout\n");
   //NOT_IMPLEMENTED();
}

int fib(int i);

/*********************************************************************
 *
 *  StartProfiling, StopProfiling
 *
 *   Profiling hooks. This is your place to inspect and modify the profiled
 *   function.
 *
 *********************************************************************/

void
StartProfiling(void *func)
{
    uint8_t *func_ptr;
    func_ptr = (uint8_t *) func;

    /*
     * TODO: Add your instrumentation code here.
     */

     // part B
     uint8_t *ret_ptr;
     ret_ptr = (uint8_t)&retCallout;

     uint8_t offset = ret_ptr - &func_ptr[5];

     printf("addr func_ptr[5] = %p\n", &func_ptr[5]);// call xx xx xx xx -> pc
     printf("addr retCallout  = %p\n", &retCallout); // destination addr

     printf("addr retCallout(dest) - addr func_ptr[5](src)  = %x\n", offset);
     // objdump -d assign0x03 | grep handleRetCallout.: -A20
     // objdump -d assign0x03 | grep retCallout.: -A20
     // http://shell-storm.org/online/Online-Assembler-and-Disassembler/


     func_ptr[0] = 0xe8; //call opcode
     func_ptr[1] = offset; // relative addr of retCallout
     func_ptr[2] = 0x00; // padding for the next 3 bytes
     func_ptr[3] = 0x00;
     func_ptr[4] = 0x00;

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

   StartProfiling(fib);

   value = fib(value);

   printf("%d\n", value);
   exit(0);
}

int fib(int i)
{
   if (i <= 1) {
      return 1;
   }
   return fib(i-1) + fib(i-2);
}
