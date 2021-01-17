## fib

* You need to correctly configure the following environment variables to run the program.

    - `LLVM_LIB`: the path for the directory that will contain the *MyLLVMPass.so*. 
    - `LLVM_BIN`: the path for the directory that will contain the LLVM commands.

* Run the following commands to trigger differents targets to build and analyze. 

```bash
# build fib
make all
```

```
# generate llvm assembly
make fib.ll
```

```
# run the pass and compare the different before and after applying the pass.
make diff
```
