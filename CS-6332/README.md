# CS 6332 - Systems Security and Malicious Code Analysis

## Dr. Kangkook Jee

## Assignment

### Assignment 1: 

* You need to implement different ways to link or load library functions by carrying out different parts of assignments

### Assignment 2:

* control flow hijack: 
   1. hijack the control flow of part0x01_x86 binary by overwriting the instruction pointer 
   2. craft an input to overwrite the stack with shellcode and transfer control the beginning of shellcode as main() function returns.
   3. hijack control flow by using ret2libc

### Assignment 3: 

* basic binary/code patching to build foundation for later tasks of  profiling the execution of a function using binary patching and writing a code for the basic x86/ARM disassembly

### Assignment 4:

* implement a minimal binary translator for Intel and ARM architectures respectively. Your implementation will

   1. dynamically decode instruction
   2. patch the branch (or control) instruction to switch into callout context
   3. count the number of instructions executed at runtime

### Assignment 5

* write a code transformation pass using the LLVM compilation infrastructure

   1. statically analyze LLVM bitcode by iterating over the module, functions, and basic blocks to output program statistics
   2. modify and transform the LLVM assembly (LLVM-IR) to instrument extra functionality. In this part, you will add a function logger -- fib_logger(), turned on by a special environment variable.
   3. a)obfuscate all string constants using XOR stream cipher, (b) restore its original value as it is being read and loaded into a register variable to preserve the original program semantics.
