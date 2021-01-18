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

# Part C

## Project Set-Up steps:

* project zip:`kxm180046-assign0x5.zip`
* go to `~/tools/llvm/` and extract `kxm180046-assign0x5.zip` to generate a folder `kxm180046`
* got to `kxm180046/part0x3`
* copy `MyLLVMPass/compile_myllvmpass.sh` to `~/tools/llvm/`
* copy `MyLLVMPass/run_myllvmpass.sh` to `~/tools/llvm/`
* copy `MyLLVMPass/Makefile` to `~/tools/llvm/src/lib/Transforms/MyLLVMPass/Makefile`
* copy `MyLLVMPass/MyLLVMPass.cpp` to `~/tools/llvm/src/lib/Transforms/MyLLVMPass/MyLLVMPass.cpp`
* copy `MyLLVMPass/MyLLVMPass.exports` to `~/tools/llvm/src/lib/Transforms/MyLLVMPass/MyLLVMPass.exports`
* copy `MyLLVMPass/CMakeLists.txt` to `~/tools/llvm/src/lib/Transforms/MyLLVMPass/CMakeLists.txt`

## To generate LL file for db_connector

* go to `kxm180046-assign0x5/part0x3/db_connector`
* run `make clean`
* run `make`
* run `clang -S -emit-llvm -m32 db_connector.c`

## To COMPILE the shared LIBRARY:

* go to `~/tools/llvm/`
* run $ `./compile_myllvmpass.sh` 
* the compiled library loc: `~/tools/llvm/build/Release+Asserts/lib/MyLLVMPass.so`

## To RUN

* go to `~/tools/llvm/`
* run `./run_myllvmpass.sh kxm180046-assign0x5/part0x3/db_connector/db_connector.ll`

# Main Idea

## Encryption
* Go through the entire module: runOnModule
* get the global list: M.getGlobalList()
* see if it is initialized: G.hasInitializer()
* and if the global is a string `G.getName().str().find("str")`
* get the initializer: `Value* newValue = G.getInitializer();`
* call the xor: `xorCipher(_dst, _src)`;
* set the new encrypted init: `G.setInitializer(const_array);`

## Decryption
* go though the inst int BB in the functions in the module: `Instruction &i: bb`
* see if it is a load or call: `isa<LoadInst>(i)` or `isa<CallInst>(i)`
* see the operand : `i.getOperand(0)`
* also check if it is a GOP `isa<GEPOperator>(i.getOperand(0)`
* get the operator to find the operand array: `GEPOperator *gepo = dyn_cast<GEPOperator>(i.getOperand(0));`
* * then we will call the xor func:
```
... create a funcTy a fiblogger definition
Constant* hook = M.getOrInsertFunction("xor", funcTy);
std::vector<Value*> args;

... populate the args and insert the new call inst. before call to fib()
auto *newInst = CallInst::Create(hook,args);
bb.getInstList().insert(i, newInst);
```