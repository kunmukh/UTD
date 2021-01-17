# Kunal Mukherjee
# CS 6332
# 11/27/20
# Assignment 5

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





