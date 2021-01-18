
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <limits.h>

#include "macros.h"
#include "arm_context.h"
#include "arm_disas.h"

/* addresses of asm callout glue code */
extern void *blCallout;
extern void *bCallout;
extern void *bxCallout;
extern void *bgtCallout;
void *callTarget;

extern int user_prog(int);

void StartProfiling(void *func);

void StopProfiling(void);

void armDecode(uint8_t *ptr, ARMInstr *instr);

void *callTarget;


/*********************************************************************
 *
 *  callout handlers
 *
 *   These get called by asm glue routines.
 *
 *********************************************************************/
void
handleBlCallout(SaveRegs *regs) {
    NOT_IMPLEMENTED();
}

void
handleBCallout(SaveRegs *regs) {
    NOT_IMPLEMENTED();
}

void
handleBxCallout(SaveRegs *regs) {
    NOT_IMPLEMENTED();
}

void
handleBgtCallout(SaveRegs *regs) {
    NOT_IMPLEMENTED();
}

void
handleRetCallout(SaveRegs *regs) {
    NOT_IMPLEMENTED();
}

/*********************************************************************
 *
 *  arm32Decode
 *
 *   Decode an IA32 instruction.
 *
 *********************************************************************/
void
armDecode(uint8_t *ptr, ARMInstr *instr)
{
   // inst length  initialized
   instr->len=0;

   instr->opcode = (uint16_t) ptr[3];
   instr->len = instr->len + 4;

   return;

}

/*********************************************************************
 *
 *  StartProfiling, StopProfiling
 *
 *   Profiling hooks. This is your place to inspect and modify the profiled
 *   function.
 *
 *********************************************************************/
void profileFunc(void *func) {
	// profileFunc runs through the opcode until it finds "c3", and then it stops.
	int i = 0;

	while(1) {

		ARMInstr *inst = malloc(sizeof(ARMInstr));
		armDecode((func+i), inst);

		printf("addr: %p, opcode: %x, len: %d\n", func+i, inst->opcode, inst->len);

		uint8_t *addr;
		addr = (uint8_t *) func+i;

		//printf("%x %x %x %x \n", addr[3], addr[2], addr[1], addr[0]);
		if  ((addr[3] == 0xe1) && 
		     (addr[2] == 0x2f) && 
		     (addr[1] == 0xff) && 
		     (addr[0] == 0x1e)) {
			free(inst);
			break;
		}
		i+=inst->len;
		free(inst);
	}
}

void
StartProfiling(void *func) {
    /*
     * TODO: Add your instrumentation code here.
     */
    profileFunc(func);
}

void
StopProfiling(void) {
    /*
     * TODO: Add your instrumentation code here.
     */
}

int main(int argc, char *argv[]) {
    int value;
    char *end;

    char buf[16];

    if (argc != 1) {
        fprintf(stderr, "usage: %s\n", argv[0]);
        exit(1);
    }

    printf("input number: ");
    scanf("%15s", buf);

    value = strtol(buf, &end, 10);

    if (((errno == ERANGE)
         && ((value == LONG_MAX) || (value == LONG_MIN)))
        || ((errno != 0) && (value == 0))) {
        perror("strtol");
        exit(1);
    }

    if (end == buf) {
        fprintf(stderr, "error: %s is not an integer\n", buf);
        exit(1);
    }

    if (*end != '\0') {
        fprintf(stderr, "error: junk at end of parameter: %s\n", end);
        exit(1);
    }

    StartProfiling(user_prog);

    value = user_prog(value);

    StopProfiling();

    printf("%d\n", value);
    exit(0);
}



