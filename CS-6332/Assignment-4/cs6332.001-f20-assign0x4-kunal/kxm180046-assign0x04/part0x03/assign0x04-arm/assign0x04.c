
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <limits.h>
#include <string.h>


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

uint8_t *startFibAddr;

// global variable.
void *callTarget;

// Original contents of memory that we patch
uint8_t *patchedAddr;
uint32_t patchedFourBytes; // 4 bytes
uint8_t patchedFourB[4];

int bCount = 0;
int bxCount = 0;
int blCount = 0;
int bgtCount = 0;

struct basicBlock {
	int countInst;
	uint32_t startingAddr;
};
struct basicBlock blockB;

// Solution prototypes
void patchToCallout(uint8_t *addr, ARMInstr instr);
void restoreInstr();
int patchNextCFlow(uint8_t *addr);


/*********************************************************************
 *
 *  callout handlers
 *
 *   These get called by asm glue routines.
 *
 *********************************************************************/

void
handleBCallout(SaveRegs *regs) {
    //NEED_TO_IMPLEMENT("Inside callout.");
    printf(":) Inside BCallout\n");
    restoreInstr();

    uint8_t * nextInst = 0;
    nextInst = patchedAddr + 8; // due to ARM pipeline.
    int32_t offset = 0x00ffffff & patchedFourBytes;

    // negative value in 2's complement encoding.
    if (BIT(offset, 23)) {
        offset |= 0xff000000;
    }

    offset <<=2;  // 4 bytes align.
    nextInst += offset;

    // return to nextInst
    regs->retPC = nextInst;
    
    patchNextCFlow(nextInst);

    printf("Patched *B\n");
}

void
handleBxCallout(SaveRegs *regs) {
    //NEED_TO_IMPLEMENT("inside callout.");
	printf(":) Inside BxCallout\n");
    
	restoreInstr();

    // return to nextInst
    regs->retPC = regs->lr;

    if (regs->lr <= startFibAddr){
    	patchNextCFlow(regs->lr);
    }

    printf("Patched *BX\n");
}

void
handleBgtCallout(SaveRegs *regs) {
	printf(":) Inside BgtCallout\n");
    restoreInstr();

    uint8_t * nextInst = 0;

    #define _Z 30
    #define _N 31
    #define _V 28

    // Branch taken:  [Reason: !Z && N==V]
    if (!BIT(regs->CPSR, _Z) 
            && (BIT(regs->CPSR, _N) == BIT(regs->CPSR, _V))) {
        // branch to the target.
        nextInst = patchedAddr + 8; // due to ARM pipeline.
        int32_t offset = 0x00ffffff & patchedFourBytes;

        // negative value in 2's complement encoding.
        if (BIT(offset, 23)) {
            offset |= 0xff000000;
        }

        offset <<=2;  // 4 bytes align, X4
        nextInst += offset;
    }
    // Ffallthrough to next instruction.
    else {
        nextInst = patchedAddr + 4;
    }

    // return to nextInst
    regs->retPC = nextInst;

    if (nextInst != (uint8_t *)  &StopProfiling)
        patchNextCFlow(nextInst);
}

void
handleBlCallout(SaveRegs *regs) {
	printf(":) Inside BlCallout\n");
    restoreInstr();

    uint8_t * nextInst = 0;
	nextInst = patchedAddr + 8; // due to ARM pipeline.
	int32_t offset = 0x00ffffff & patchedFourBytes;

    // negative value in 2's complement encoding.
    if (BIT(offset, 23)) {
        offset |= 0xff000000;
    }

	offset <<=2;  // 4 bytes align.
	nextInst += offset;

    // return to nextInst
    regs->retPC = nextInst;

    
    if (nextInst != (uint8_t *)  &StopProfiling)
        patchNextCFlow(nextInst);
}

void __patchToCallout(uint8_t *addr, ARMInstr instr) {
    // Save original code so we can restore it later
    patchedAddr = addr;
    patchedFourBytes = *(uint32_t * )(addr);
    printf("patch addr%p %x\n", addr, patchedFourBytes);
    //memcpy(patchedFourB, addr, 4);


    void *call_target = NULL;
    char *inst_name = NULL;

    uint8_t br_inst = 0;

    printf("\n\naddr: %p opcode: %x\n", addr, instr.opcode);
    blockB.startingAddr = addr;

    if (IS_ARM_BL(instr.opcode)) {
        printf(":) Inside BL\n");
        inst_name = "BL";
        call_target = &blCallout;
        br_inst = ARM_BL;
        blCount++;

    } else if (IS_ARM_BX(instr.opcode)) {

        //NEED_TO_IMPLEMENT("transfer to bxCallout");
        printf(":) Inside *BX\n");
        inst_name = "BX";
        call_target = &bxCallout;
        br_inst = ARM_B;
        bxCount++;

    } else if (IS_ARM_BGT(instr.opcode)) {

        //NEED_TO_IMPLEMENT("transfer to bxCallout");
        printf(":) Inside *BGT\n");
        inst_name = "BGT";
        call_target = &bgtCallout;
        br_inst = ARM_BL;
        bgtCount++;

    } else if (IS_ARM_B(instr.opcode)) {

        //NEED_TO_IMPLEMENT("transfer to bxCallout");
        printf(":) Inside *B\n");
        inst_name = "B";
        call_target = &bCallout;
        br_inst = ARM_BL;
        bCount++;

    }
    else {
        // we are only covering instructions fromn
        // fib()
        NOT_REACHED();
    }

    // offset calculation and little endian encoding.

    int32_t offset = (int32_t) call_target - (int32_t)(addr + 8);
    offset >>= 2; // word (two-bytes) aligned 

    uint8_t *_offset = (uint8_t * ) & offset;

    addr[0] = _offset[0];
    addr[1] = _offset[1];
    addr[2] = _offset[2];
    addr[3] = br_inst; // BL instr.

    __builtin___clear_cache((void *) addr, (void *) (addr + 4));
}

/*
 * Restores the code last patched by patch_in_call_to_me. If that function
 * wasn't called, something bad will probably happen.
 */
void restoreInstr() {

    printf("restore called :)\n");
    //NEED_TO_IMPLEMENT("unpatch by restoring previously cached instructions.");
    //printf("Addr: %8x %8x\n", (int8_t *)patchedAddr, (int32_t *)patchedFourBytes);

    uint8_t *patchedFourBytesT = (uint8_t * ) & patchedFourBytes;

    patchedAddr[0] = patchedFourBytesT[0];
    patchedAddr[1] = patchedFourBytesT[1];
    patchedAddr[2] = patchedFourBytesT[2];
    patchedAddr[3] = patchedFourBytesT[3];


    __builtin___clear_cache((void *) patchedAddr, (void *) (patchedAddr + 8));
}

int patchNextCFlow(uint8_t *addr) {
    ARMInstr instr;
    int cnt = 1;
    

    while (1) {
        armDecode(addr, &instr);
        printf("opcode: %x cnt:%d\n", instr.opcode, cnt);
        if ((IS_ARM_CFLOW(instr.opcode)) || 
            (*(uint32_t*)addr == ARM_BX_INST)) { //control flow 
            printf("start addr: %p cntrl opcode: %x cnt:%d\n", blockB.startingAddr ,instr.opcode, blockB.countInst);
            blockB.countInst = 1;
            //printf("Inside CF\n");

            break;
        }

        cnt ++;
        blockB.countInst = cnt;
        addr += instr.len;
    }

    __patchToCallout(addr, instr);
    return cnt;
}

/*********************************************************************
 *
 *  arm32Decode
 *
 *   Decode an ARM instruction.
 *
 *********************************************************************/

void
armDecode(uint8_t *ptr, ARMInstr *instr) {
    int32_t inst = *((uint32_t *) ptr);

    //printf("%8x\n", inst);
    
    // condition prefix
    instr->cond =   (uint8_t) BITS(inst, 28, 31);  // 4-bits
    // 2nd and 3rd bytes after condition prefix
    instr->opcode = (uint8_t) BITS(inst, 24, 31);  // 8-bits //FIX
    instr->len = 4;
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
StartProfiling(void *func) {
	startFibAddr = (uint8_t*)func;
    printf("\n\n***Patching Start\n\n");
    patchNextCFlow(func);
}

void
StopProfiling(void) {
    //NEED_TO_IMPLEMENT("Clean-up needed.");
	restoreInstr();
	printf("start addr: %p cnt:%d\n", blockB.startingAddr , blockB.countInst);
    printf("\nbCount: %d\nblCount: %d\nbgtCount: %d\nbxCount: %d\n", 
    	bCount, blCount, bgtCount*2, bxCount);
    printf("\n\n***Patching Done\n\n");
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

