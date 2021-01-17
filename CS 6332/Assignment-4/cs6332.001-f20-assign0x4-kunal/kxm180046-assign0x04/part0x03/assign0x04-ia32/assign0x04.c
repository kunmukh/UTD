#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <limits.h>
#include <string.h>
#include <unistd.h>

#include "macros.h"
#include "ia32_context.h"
#include "ia32_disas.h"

/* addresses of asm callout glue code */

extern void *jccCallout;
extern void *jmpCallout;
extern void *callCallout;
extern void *retCallout;

extern uint32_t ia32DecodeTable[]; /* see beylow */

// Kunal Added
void *patchedAddr;
uint8_t patchedFiveBytes [5];
void *nextPatchedAddr;

uint32_t EQ = 0x246;
uint8_t *startFibAddr;

struct basicBlock {
	int countInst;
	uint32_t startingAddr;
};

int jccCount = 0;
int retCount = 0;
int callCount = 0;
int jmpCount = 0;

struct basicBlock blockB;

void unpatch();
void patchedNextBranch(void* func);

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
 *assign0x04.c
 *********************************************************************/
void unpatchInstr() {
    memcpy(patchedAddr, patchedFiveBytes, 5);
}

void
handleJccCallout(SaveRegs regs) {
    //NOT_IMPLEMENTED();
    printf("Inside JCC Callout\n");
    unpatchInstr();

    regs.pc = patchedAddr;
    if (regs.eflags >= EQ) { //less than 1
        patchedNextBranch(nextPatchedAddr);
    } else {
        patchedNextBranch(nextPatchedAddr + patchedFiveBytes[1]);
    }
}

void
handleJmpCallout(SaveRegs regs) {
    //NOT_IMPLEMENTED();
    printf("Inside JMP Callout\n");
    unpatchInstr();

    regs.pc = nextPatchedAddr + patchedFiveBytes[1];
    
    patchedNextBranch(nextPatchedAddr + patchedFiveBytes[1]);

}

void
handleCallCallout(SaveRegs regs) {
    //NOT_IMPLEMENTED();    
    printf("Inside CALL Callout\n");
    unpatchInstr();

    uint32_t offset;
    memcpy(&offset, patchedFiveBytes+1, 4);
    callTarget = nextPatchedAddr + offset;

    patchedNextBranch(callTarget);

}

void
handleRetCallout(SaveRegs regs) {
    //NOT_IMPLEMENTED();
    printf("Inside RET Callout\n");
    unpatchInstr();

    if (regs.retPC >= startFibAddr){
        printf("RET inside StopProfiling\n");    
        patchedNextBranch(regs.retPC);

    }

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
   
}

/*********************************************************************
 *
 *  StartProfiling, StopProfiling
 *
 *   Profiling hooks. This is your place to inspect and modify the profiled
 *   function.
 *
 *********************************************************************/
void
patchedNextBranch(void *func){

    int flag = 0;

    uint8_t * currentPtr = func;

    while (!flag){
        IA32Instr *inst = malloc(sizeof(IA32Instr));
        ia32Decode(currentPtr, inst);
        blockB.startingAddr = currentPtr;

        //printf("addr: %p, opcode: %x, len: %d\n", currentPtr, inst->opcode, inst->len);
        
        if (inst->opcode == 0xc3) {
            printf("Basic Block Instr: startInst: 0x%x Inst-count:%x\n", blockB.startingAddr, blockB.countInst);
        	printf("0xc3 Opcode found...\n\n\n");
            flag = 1;
            blockB.countInst = 0;
        }
        
        if (IS_DECODE(inst->opcode, IA32_CFLOW)){

            patchedAddr = currentPtr;
            memcpy(patchedFiveBytes, currentPtr, 5);
            nextPatchedAddr = currentPtr + (inst->len);

            uint8_t *callptr;
            printf("patched addr: %p and patched bytes: %x\n", currentPtr, *(int *)patchedFiveBytes);
            
            if (IS_DECODE(inst->opcode, IA32_RET)){
                printf("*RET at %p opc: %x\n", currentPtr, inst->opcode);
                callptr = (uint8_t*)&retCallout;
                retCount++;

            } else if (IS_DECODE(inst->opcode, IA32_JCC)) {
                printf("*JCC at %p opc: %x\n", currentPtr, inst->opcode);
                callptr = (uint8_t*)&jccCallout;
                jccCount++;

            } else if (IS_DECODE(inst->opcode, IA32_JMP)) {
                printf("*JMP at %p opc: %x\n", currentPtr, inst->opcode);
                callptr = (uint8_t*)&jmpCallout;
                jmpCount++;

            } else if (IS_DECODE(inst->opcode, IA32_CALL)) {
                printf("*CALL at %p opc: %x\n", currentPtr, inst->opcode);
                callptr = (uint8_t*)&callCallout;
                callCount++;

            }

            // printf("current addr: %p op:%x\n",  currentPtr, currentPtr[0]);
            // printf("current+5 addr: %p\n",  currentPtr+5);            
            // printf("callptr: %p\n", callptr);

            int32_t offset = callptr - (currentPtr+5);
            printf("offset: %x\n", offset);

            // patch the code
            currentPtr[0] = 0xe8;
            memcpy(currentPtr+1, &offset, 4);           

            flag = 1;
            blockB.countInst++;
            
        }
        currentPtr = currentPtr + inst->len;
        free(inst);
    }

    printf("Patching Done\n");
    return;
}

void
StartProfiling(void *func) {
    // StartProfile calls a new helper func profileFunc()
    startFibAddr = (uint16_t*)func;
    printf("\n\n***Profiling Started***\n");
    patchedNextBranch(func);
    
    return;
}

void
StopProfiling(void) {
    unpatchInstr();
    printf("Basic Block Instr: startInst: 0x%x Inst-count:%x\n", blockB.startingAddr, blockB.countInst);
    printf("\njcc count: %d\njmp count: %d\ncall count: %d\nret count: %d\n", 
    	jccCount, jmpCount, callCount/2, retCount/2);
    printf("\n\n***Profiling Done***\n");
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
