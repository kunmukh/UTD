# Kunal Mukherjee
# CS 6332
# 11/27/20
# Assignment 5

# Part A

## Project Set-Up steps:

* project zip:`kxm180046-assign0x5.zip`
* go to `~/tools/llvm/` and extract `kxm180046-assign0x5.zip` to generate a folder `kxm180046`
* got to `kxm180046/part0x1`
* copy `MyLLVMPass/compile_myllvmpass.sh` to `~/tools/llvm/`
* copy `MyLLVMPass/run_myllvmpass.sh` to `~/tools/llvm/`
* copy `MyLLVMPass/Makefile` to `~/tools/llvm/src/lib/Transforms/MyLLVMPass/Makefile`
* copy `MyLLVMPass/MyLLVMPass.cpp` to `~/tools/llvm/src/lib/Transforms/MyLLVMPass/MyLLVMPass.cpp`
* copy `MyLLVMPass/MyLLVMPass.exports` to `~/tools/llvm/src/lib/Transforms/MyLLVMPass/MyLLVMPass.exports`
* copy `MyLLVMPass/CMakeLists.txt` to `~/tools/llvm/src/lib/Transforms/MyLLVMPass/CMakeLists.txt`

## To generate LL file for Fib

* go to `kxm180046-assign0x5/part0x1/fib`
* run `make clean`
* run `make`
* run `clang -S -emit-llvm -m32 fib.c`

## To COMPILE the shared LIBRARY:

* go to `~/tools/llvm/`
* run $ `./compile_myllvmpass.sh` 
* the compiled library loc: `~/tools/llvm/build/Release+Asserts/lib/MyLLVMPass.so`

## To RUN

* go to `~/tools/llvm/`
* run `./run_myllvmpass.sh kxm180046-assign0x5/part0x1/fib/fib.ll`

# Main Idea

* You run through modules by using runOnModule() and functions using runOnFunction()
* use M.getGlobalList(): to get the global variables
* use G.hasInitializer(): to see if it is initialized
* use G.getInitializer(): to get the initialized value
* use F.getType(): to get the func proto type
* use F.getName(): to get the func name
* use F.getReturnType(): to get the func return type
* use i.getOpcodeName(): to get the opcode
* use opCounter.begin()->second: to get the operand



