# Assignment 0x04 (70 pt)

This assignment extends your work on the [previous assignment][assignment0x3]. The assignment aims to  implement a minimal [binary translator] for Intel and ARM architectures respectively. Your implementation will (1) dynamically decode instruction, (2) patch the branch (or control) instruction to switch into callout context, (3) count the number of instructions executed at runtime. 

Although assignment is is tested and verified for GCC version 7, 8 compilers, the other environmental factors may affect compilers to generate different machine instruction sequences, which may result in runtime failures. Please feel free to consult to the instructor or TA regarding such issues. 

## How to submit the assignment.

* The assignment will due on **Nov 20, 11:59 PM**. Please submit via eLearning.  

* Please create a folder with `<netid>-assign0x04` with the following structure to submit the assignment.
You will extend the provided skeleton codes to complete each part. Each folder will contain the necessary source files to reproduce your work. Please do not forget to write a README.md document to describe your solution. After completing the assignment, compress the folder and submit the file to eLearning.

```
<netid>-assign0x04/
├── part0x01/
│   ├── assign0x4-ia32
│   ├── assign0x4-arm
├── part0x02/
│   ├── assign0x4-ia32
│   ├── assign0x4-arm
├── part0x03/
│   ├── assign0x4-ia32
│   ├── assign0x4-arm
└── README.md
```

## Part1: Instruction Decode (20 pt)

Length of the instruction, determining Control Flow Instructions.

**[IA32 (i386): 15 pt]**: The goal of this step is to use *[StartProfiling()]* to decode a block of instructions. You need only to decode enough of each instruction to determine its length. By doing this you should be able to decode a block of instructions of arbitrary length. *[StartProfiling()]* should print the address, opcode, and length of instructions for *[fib()]* until it encounters `ret` (0xc9) instruction. 

Use the pseudocode from the lecture slide as a guide. An IA32 opcode map has been provided in *[ia32DecodeTable]* to save having to type all this out. Use it as you see fit.

**[IA32 (ARM): 5 pt]**: It is relatively simpler to disassembly ARM instructions due to the fixed-width alignment scheme of ARM architecture; four-bytes and two-bytes alignments for ARM and Thumb modes respectively. Similarly, you need to add ARM decoder code to *[StartProfiling()]* to print the address, opcode, and length of instructions for *[fib()]* until it meets `bx lr` (0xe12fff1e). 

**[Think item]** Can we differentiate [ARM and thumb mode statically][arm-vs-thumb], by only looking at binary sequence?

## Part2: Control Flow Following (30 pt: IA32 15 pt + ARM 15 pt)
You should now have the tools to follow the execution of control flow. To do this decode the instructions to be executed until you hit a control flow instruction. Binary patch that instruction to call you instead of doing the control flow. You can then return to the code knowing that you will be called before execution passes that point. When your handler is called, unpatch the instruction, emulate its behavior and binary patch the end of the next basic block.

For each basic block you encounter, dump the instructions in that block in the same format as in step 1. You should stop this process when you hit the StopProfiling function.

## Part3: Counting basic block and instruction executions (20 pt: IA32 10 pt + ARM 10 pt)

Create a data structure to capture the start address each basic block executed and number of instructions. Run target program (fib()) with different inputs and check the number of instructions (and basic blocks) executions.

---
[assignment0x3]:http://syssec0.utdallas.edu/utd-classes/cs6332.001-f20-assign0x3
[StartProfiling()]:assign0x04-ia32/assign0x04.c#L85
[fib()]:http://syssec0.utdallas.edu/utd-classes/cs6332.001-f20-assign0x3
[ia32DecodeTable]:assign0x04-ia32/ia32_disas.c#L19
[arm-vs-thumb]:https://elixir.bootlin.com/linux/latest/source/arch/arm/include/asm/opcodes.h#L56
[binary translator]:http://season-lab.github.io/papers/sok-dbi-ASIACCS19.pdf
