#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <limits.h>

#include "macros.h"
#include "ia32_context.h"
#include "ia32_disas.h"

/* addresses of asm callout glue code */

extern void *jccCallout;
extern void *jmpCallout;
extern void *callCallout;
extern void *retCallout;

extern uint32_t ia32DecodeTable[]; /* see below */

/* instrumentation target */

extern int user_prog(int);

void StartProfiling(void *func);

void StopProfiling(void);

void ia32Decode(uint8_t *ptr, IA32Instr *instr);

void *callTarget;

// copied from Dr.Jee: https://codimd.syssec.org/s/H13-jWUtH
#define IS_DECODE(_a, _b)   (ia32DecodeTable[ (_a) ]& (_b) )

/*********************************************************************
 *
 *  callout handlers
 *
 *   These get called by asm glue routines.
 *
 *********************************************************************/

void
handleJccCallout(SaveRegs regs) {
    NOT_IMPLEMENTED();
}

void
handleJmpCallout(SaveRegs regs) {
    NOT_IMPLEMENTED();
}

void
handleCallCallout(SaveRegs regs) {
    NOT_IMPLEMENTED();
}

void
handleRetCallout(SaveRegs regs) {
    NOT_IMPLEMENTED();
}



/*********************************************************************
 *
 *  ia32Decode
 *
 *   Decode an IA32 instruction.
 *
 *********************************************************************/

// copied from Dr.Jee: https://codimd.syssec.org/s/H13-jWUtH
// use lecture 12: slide 16-22 to understand how to handle the opcode and the length
void
ia32Decode(uint8_t *ptr, IA32Instr *instr)
{
	instr->len=0;
	int i = 0; // index variable

 	//parse prefixes
  	while (IS_DECODE(ptr[i], IA32_PREFIX)) {

        instr->len = instr->len + 1;
		i++;
   	}

   	//processing opcode size 1 byte or 2 byte case
   	if (IS_DECODE(ptr[i], IA32_2BYTE)) {

   		instr->len = instr->len + 2;
		instr->opcode = (uint16_t) ptr[i];
		i+=2;
    
    } else {

		instr->len = instr->len + 1;
		instr->opcode = (uint16_t) ptr[i];
		i++;
	}
	

   if (IS_DECODE(instr->opcode, IA32_MODRM)) {
        
        switch (BITS(ptr[i],6,7)){  // Checking MOD value
            case 0b00:  // 0

                instr->len = instr->len + 1;
				i++;

				if(BITS(ptr[i],0,2) == 4){ //0100
					instr->len = instr->len + 1;
					i++;		
				}
				if(BITS(ptr[i],0,2) == 5){ //0101
					instr->len = instr->len + 4;
					i+=4;		
				}
			break;
            case 0b01:     // 1

                instr->len = instr->len + 2;
				i+=2;

				if(BITS(ptr[i],0,2) == 4){
					instr->len = instr->len + 1;
					i++;		
				}
			break;
            case 0b10:     // 2

                instr->len = instr->len + 6;
				i+=6;
			break;
            case 0b11:     // 3

				instr->len = instr->len + 1;
				i++;
            break;
        }
    }

    if (IS_DECODE(instr->opcode, IA32_IMM8)) {

        instr->len = instr->len + 1;
    } else if (IS_DECODE(instr->opcode, IA32_IMM32)){

        instr->len = instr->len + 4;
	}
	
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
		
		IA32Instr *inst = malloc(sizeof(IA32Instr));
		ia32Decode((func+i), inst);

		printf("addr: %p, opcode: %x, len: %d\n", func+i, inst->opcode, inst->len);
		
		if (inst->opcode == 0xc3) {
			free(inst);
			break;
		}
		i+=inst->len;
		free(inst);
	}
}

void
StartProfiling(void *func) {
    // StartProfile calls a new helper func profileFunc()
    profileFunc(func);
}

void
StopProfiling(void) {
    ;
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



