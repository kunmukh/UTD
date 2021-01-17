# Kunal Mukherjee
# CS 6332
# 11/27/20
# Assignment 5

# Part B

## Project Set-Up steps:

* project zip:`kxm180046-assign0x5.zip`
* go to `~/tools/llvm/` and extract `kxm180046-assign0x5.zip` to generate a folder `kxm180046`
* got to `kxm180046/part0x2`
* copy `MyLLVMPass/compile_myllvmpass.sh` to `~/tools/llvm/`
* copy `MyLLVMPass/run_myllvmpass.sh` to `~/tools/llvm/`
* copy `MyLLVMPass/Makefile` to `~/tools/llvm/src/lib/Transforms/MyLLVMPass/Makefile`
* copy `MyLLVMPass/MyLLVMPass.cpp` to `~/tools/llvm/src/lib/Transforms/MyLLVMPass/MyLLVMPass.cpp`
* copy `MyLLVMPass/MyLLVMPass.exports` to `~/tools/llvm/src/lib/Transforms/MyLLVMPass/MyLLVMPass.exports`
* copy `MyLLVMPass/CMakeLists.txt` to `~/tools/llvm/src/lib/Transforms/MyLLVMPass/CMakeLists.txt`

## To generate LL file for Fib

* go to `kxm180046-assign0x5/part0x2/fib`
* run `make clean`
* run `make`
* run `clang -S -emit-llvm -m32 fib.c`

## To COMPILE the shared LIBRARY:

* go to `~/tools/llvm/`
* run $ `./compile_myllvmpass.sh` 
* the compiled library loc: `~/tools/llvm/build/Release+Asserts/lib/MyLLVMPass.so`

## To RUN

* go to `~/tools/llvm/`
* run `./run_myllvmpass.sh kxm180046-assign0x5/part0x2/fib/fib.ll`

# Main Idea

* we will iterate over the whole module by runOnModule()
* we will find if it a "ret" or a "fib" call inst
* ret check: if `i.getOpcodeName().compare("ret") == 0 `
* call check: `isa<CallInst>(i) && cast<CallInst>(i).getCalledFunction()->getName().compare("fib") == 0`

* then we will call the fiblogger func:
```
... create a funcTy a fiblogger definition
Constant* hook = M.getOrInsertFunction("fib_logger", funcTy);
std::vector<Value*> args;

... populate the args and insert the new call inst. before call to fib()
auto *newInst = CallInst::Create(hook,args);
bb.getInstList().insert(i, newInst);
```



