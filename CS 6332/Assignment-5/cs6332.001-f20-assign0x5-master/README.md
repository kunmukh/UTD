# cs6332-001: assignment0x5 (90 pt + bonus 20 pt)

In this assignment, you will write a code [transformation pass] using [the LLVM compilation infrastructure][llvm]. We will use the the LLVM version 3.4 for this assignment. You should have access to [the installation and basic usage guide]. To assist you, we also prepared the comprehensive sets of [LLVM 3.4 documentations][llvm3.4-docs] and its [API illustration][llvm-3.4 doxygen]. You will extent the provided skeleton code ([MyLLVMPass/](MyLLVMPass)) to do each part.

## How to submit the assignment.

The assignment will be due on **Dec 9, 11:59 PM**. Please submit via [eLearning].

Please create `<your-netid>-assign0x05` folder with the following structure to submit the assignment.
You will extend the [MyLLVMPass.cpp] to complete each part. Each folder will contain the necessary source files needed to reproduce your work. Please do not forget to write a README.md document to describe your solution. After completing the assignment, compress the folder and submit the file to [eLearning].

```
<your-netid>-assign0x5 
├── part0x1
│   ├── MyLLVMPass.cpp
│   └── README.md
├── part0x2
│   ├── MyLLVMPass.cpp
│   └── README.md
├── part0x3
│   ├── MyLLVMPass.cpp
│   └── README.md
├── part0x4
│   ├── MyLLVMPass.cpp
│   └── README.md
├── part0x5
│   ├── MyLLVMPass.cpp
│   └── README.md
└── README.md
```

## Re-visiting [fib()]

### Part0x1: Static profiling with LLVM (10 pt)

In this part, you will extend the [MyLLVMPass.cpp] to *statically* analyze LLVM bitcode by iterating over the [module], [functions][Function], and [basic blocks][BasicBlock] to output program statistics of the following.

1. For the [Module],
    * Enumerate all [global variables] and their [types][Type] and their values (if initialized).
    * Enumerate all included [functions][Function] and their [prototype][FunctionType]. 

2. For each [Function],
    * List [input parameters][Argument] along with their [types][Type].
    * Function return type.
    * Number of [basic blocks][BasicBlock] included.

3. For each [basic block][BasicBlock], 
    * Number of [instructions][Instruction] included.
    * [Instruction] summary in the following format.
    ```
    InstName: CallInst, Operand #: 2
    ...
    ```

### Part 0x2: adding debug functions (20 pt)

Now we are about to modify and transform the LLVM assembly (LLVM-IR) to instrument extra functionality. In this part, you will add a function logger -- [fib_logger()], turned on by [a special environment variable](). The pass will instrument LLVM assembly to append the call to the [fib_logger()] before the instruction that *calls* to [fib()] and *ret* instruction inside [fib()]. The LLVM transform will look similar to this.

![](/uploads/upload_1d5ac181a86c5f1fd5a1439a1a38dbd5.png)

<div id="doc" class="markdown-body container-fluid"><p><img src="https://codimd.syssec.org/uploads/upload_1d5ac181a86c5f1fd5a1439a1a38dbd5.png" alt="" class="md-image md-image"></p></div>

## [DB connector][db_connector] program

From this part of the assignment, we will move on to play with a realistic program that performs something useful. As shown, [db_connector] program automates the [Postgres database] connection processing by caching your credential seeking to save your time to type in over and over again. As the original program comes with a few security defects, our goal here is to write a [transformation pass] that would harden the output binary.

### Part 0x3: Encrypting static symbols (30 pt)

[db_connector.c] contains multiples of hard-coded strings that the attacker can easily exploit. For instance, the attacker can run [strings] command against the output binary to extract the [default password] encoded in a plain-text. Our goal in this part is to (1) obfuscate all [string constants][string constant] using [XOR stream cipher][xorCipher()], (2) restore its original value as it is being [read and loaded][load] into a register variable to preserve the original program semantics.

Module class has the global variables as its member which you can iterate or access using [global iterator] or [LLVMGetFirstGlobal()], [getGlobalList()]methods. For each global variables, use [LLVMGetInitializer()] and [LLVMSetInitializer()] methods to retrieve and update the encrypted value.

You also need to decrypt the string constant before it is loaded into the memory. You can also enumerate [User] instructions for each [Value] class. [Value] class has public member function to enumerate its [Users()]. Please prepend a call to [xorCipher()] before every [load] [instruction][loadInst] that would refer to encrypted variables and substitute its input operand decrypted data.

### Part 0x4: Minimizing the sensitive data exposure (30 pt)

From the previous part, global string constants are decrypted as soon as they are loaded into the memory, which may prolong the data exposure in address space for an arbitrary amount of time. The user (or attacker) has control over time. In this assignment, we want to extend the secrecy of encrypted data by statically tracking the information flow.

For each global variable, you will trace the use-def chain using the LLVM interface until the value is transformed and become an input to another function. Please note that *getelementptr* only calculates the reference without modifying the data.

### Part 5: Link with shared library (bonus 20 pt)

We have had a bit unrealistic assumption on where to find cipher function ([xorCipher()]). As the function already exists in [utils.c], we were just to declare its linkage from [db_connector] module and call it as needed. This is untrue for realistic settings. We cannot expect your code to include necessary functions with no prior agreement. To be a realistic approach, we can consider two design choices for the compiler: *(1)* the compiler simply appends such utility functions to the target binary, *(2)* the compiler only adds function declarations and direct to find necessary symbols at runtime from shared libraries (say \*.so files). While both are valid, the second approach is more favorable since it would generate a smaller code with more flexible and modular code deployment options. The [compiler-rt] helps you implement the runtime compiler support libraries. You can use this approach to compile and build the cipher module as a seperate shared library to be called as needed.

In this part of the assignment, the compiled program will *dynamically* link to *[xorCipher()]*, exported from *libutils.so*.

<!-- sources -->
[MyLLVMPass.cpp]:MyLLVMPass/MyLLVMPass.cpp
[fib()]:fib/fib.c
[db_connector.c]:db_connector/db_connector.c
[xorCipher()]:db_connector/utils.c
[xorCipher2()]:db_connector/utils.c
[libmycipher.so]:db_connector/Makefile
[utils.c]:db_connector/utils.c
[db_connector]:db_connector
[default password]:db_connector/db_connector.c
[fib_logger()]:fib/utils.h#L5

<!-- llvm links  -->
[llvm]:https://llvm.org/
[llvm3.4-docs]:https://llvm-3.4.syssec.org/
[llvm-3.4 doxygen]:https://llvm-3.4.syssec.org/doxygen/
[LLVMGetFirstGlobal()]:https://llvm-3.4.syssec.org/doxygen/group__LLVMCoreValueConstantGlobalVariable.html#ga35ec32d09832c21269295c9686b3dfd5
[global variables]:https://llvm-3.4.syssec.org/doxygen/group__LLVMCoreValueConstantGlobalVariable.html
[global values]:https://llvm-3.4.syssec.org/doxygen/group__LLVMCCoreValueConstantGlobals.html
[LLVMGetInitializer()]:https://llvm-3.4.syssec.org/doxygen/group__LLVMCoreValueConstantGlobalVariable.html#ga9b1abdccb3c2450804dc654d6865106d
[LLVMSetInitializer()]:https://llvm-3.4.syssec.org/doxygen/group__LLVMCoreValueConstantGlobalVariable.html#gaecc937af154a1d4fd5d337e5783a8387
[getGlobalList()]:https://llvm-3.4.syssec.org/doxygen/classllvm_1_1Module.html#a28c0310f56c2ea41ff7012df55ac6dc5
[User]:https://llvm-3.4.syssec.org/doxygen/classllvm_1_1User.html
[Value]:https://llvm-3.4.syssec.org/doxygen/classllvm_1_1Value.html
[Constant]:https://llvm-3.4.syssec.org/doxygen/classllvm_1_1Constant.html
[load]:https://llvm-3.4.syssec.org/LangRef.html#load-instruction
[loadInst]:https://llvm-3.4.syssec.org/doxygen/classllvm_1_1LoadInst.html
[Function]:https://llvm-3.4.syssec.org/doxygen/classllvm_1_1Function.html
[BasicBlock]:https://llvm-3.4.syssec.org/doxygen/group__LLVMCCoreValueBasicBlock.html
[Instruction]:https://llvm-3.4.syssec.org/doxygen/classllvm_1_1Instruction.html
[transformation pass]:https://todo
[string constant]:https://todo
[Users()]:https://todo
[Module]:https://llvm-3.4.syssec.org/doxygen/classllvm_1_1Module.html
[Type]:https://llvm-3.4.syssec.org/doxygen/classllvm_1_1Type.html
[FunctionType]:https://llvm-3.4.syssec.org/doxygen/classllvm_1_1FunctionType.html
[Argument]:https://llvm-3.4.syssec.org/doxygen/classllvm_1_1Argument.html
[global iterator]:https://llvm-3.4.syssec.org/doxygen/classllvm_1_1Module.html#a0567b31cf5caa26522fcc2e7cadc1dde
[compiler-rt]:https://compiler-rt.llvm.org/
<!-- other links -->
[strings]:https://man7.org/linux/man-pages/man1/strings.1.html
[Postgres database]:https://www.postgresql.org/
[Function prototype - Wikipedia]:https://en.wikipedia.org/wiki/Function_prototype

[the installation and basic usage guide]:https://cometmail-my.sharepoint.com/:w:/g/personal/kxj190011_utdallas_edu/EbX3bz8utiVJgSn42ntNIXwBdgluWT1qgl34fOi2_Kd8xA?e=Uv2kVX

[eLearning]:https://elearning.utdallas.edu/webapps/blackboard/content/listContentEditable.jsp?content_id=_3262367_1&course_id=_180521_1&mode=reset

###### tags: `cs6332`,`llvm`,`assignment`
