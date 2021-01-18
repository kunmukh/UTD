# Kuna Mukherjee
# 11/16/20
# CS 6332
# Dr. Kangkook Jee

# Assignment 0x04 (70 pt)

## Part1: Instruction Decode (20 pt)

### arm

### armDecode 
* armDecode was simple as the inst are always 4 byte long 

### ia32

### ia32Decode 
* copied from Dr.Jee: https://codimd.syssec.org/s/H13-jWUtH
* use lecture 12: slide 16-22 to understand how to handle
* the opcode

* start profile calls a new helper func profileFunc(), that runs through the opcode until it finds "0xc3", and then it stops.

* armDecode was simple as the inst are always 4 byte long 


## Part2: Control Flow Following (30 pt: IA32 15 pt + ARM 15 pt)

### ia32

* from part1, we can get the instruction 
* so we use Dr.Jee's helper functions to first find if the instruction refer to a control flow `(IS_DECODE(inst->opcode, IA32_CFLOW))` and then what kind: 
	`(IS_DECODE(inst->opcode, IA32_RET))` or
	`(IS_DECODE(inst->opcode, IA32_JCC))` or
	`(IS_DECODE(inst->opcode, IA32_JMP))` or
	`(IS_DECODE(inst->opcode, IA32_CALL))`
* And based on that we will patch for the callout, `currentPtr[0] = 0xe8; memcpy(currentPtr+1, &offset, 4);` 
* In the callout we will first unpatch to preserve the control flow. `memcpy(patchedAddr, patchedFiveBytes, 5);`. 

### arm

* for arm everything is conceptually similar like ia32, except control flow check in done in `patchNextCFlow` and the patch is done in `__patchToCallout`. 
* * so we use Dr.Jee's helper functions to first find if the instruction refer to a control flow `((IS_ARM_CFLOW(instr.opcode)) || ((uint8_t)*addr == ARM_BX_INST))` and then what kind: 
	`(IS_ARM_BL(instr.opcode))` or
	`(IS_ARM_B(instr.opcode))` or
	`(IS_ARM_BX(instr.opcode))` or
	`(IS_ARM_BGT(instr.opcode))`
* And based on that we will patch for the callout, 
```
	addr[0] = _offset[0];
    addr[1] = _offset[1];
    addr[2] = _offset[2];
    addr[3] = br_inst; // BL instr.
```
* In the callout we will first unpatch to preserve the control flow.
```
 	patchedAddr[0] = patchedFourB[0];
    patchedAddr[1] = patchedFourB[1];
    patchedAddr[2] = patchedFourB[2];
    patchedAddr[3] = patchedFourB[3];
```

## Part3: Counting basic block and instruction executions (20 pt: IA32 10 pt + ARM 10 pt)

### arm and ia32

### ia32

* after part2, to do part 3 we will just have to create a struct to capture the starting instruction and the count. 
* when we start patching in ia32 in patchNextBranch(), we store the start address `blockB.startingAddr = currentPtr;` and increment the count `blockB.countInst++;`
* we keep doing it until the opcode we hit is `inst->opcode == 0xc3`. Then we reset the counter and repopulate the starting address. 

```
struct basicBlock {
	int countInst;
	uint32_t startingAddr;
};
```

### arm

* for arm everything is the same as ia32, except instruction count is incremented in `patchNextCFlow` and the starting address is set in `__patchToCallout`.