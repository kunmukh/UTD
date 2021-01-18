# Student Answer

* Kunal Mukherjee
* 11/5/20
* Assignment 0x3

# Assignment 0x03 (20 pt)

## Part0x01: Patching binary to return (5pt + 5pt)

### IA-32

Compiling:
```
$ make
```

Running and Output:
```
$ ./assign0x03 5
134515106
```

This assignment similar like arm but it is for IA-32. The issue here will be of opcode, as unlike ARM, the IA32 instruction set's op code is not of constant length. In this case, we want to immediately return as the function fib() is called. Dr. Jee gave us a pointer to the function, fib(). So, we basically can dereference it and use it as array to overwrite the current opcode.

So, the question is how to get the opcode. We write a function main(), which we can disassemble to get the opcode for the return, and understand how it is used. The function main() basically returns and does nothing else. So, that we can get the op code easily. From the objdump we can see the opcode for return is "retq" and the hex is "c3".

So, since we have the opcode, we just need to overwrite the opcode of fib for the first byte, and we can do that in StartProfiling(). The over write is of the form of 1 byte because for IA-32, the instruction length is of 1 byte long for "retq". 

StartProfiling
```
  	// part A
    func_ptr[0] = 0xc3;
```


The test function(`cat test.c`):
```
void main(){
    return;
}
```

The disassemble command and result (`objdump -D test | grep -A20 main:`):
```
0000000100003fb0 _main:
100003fb0: 55                           pushq %rbp
100003fb1: 48 89 e5                     movq  %rsp, %rbp
100003fb4: 5d                           popq  %rbp
100003fb5: c3                           retq
```
