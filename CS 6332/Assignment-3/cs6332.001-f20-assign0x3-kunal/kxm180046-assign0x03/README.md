# Student Answer

* Kunal Mukherjee
* 11/5/20
* Assignment 0x3

# Assignment 0x03 (20 pt)

## Part0x01: Patching binary to return (5pt + 5pt)

### ARM

Compiling:
```
$ make
```

Running and Output:
```
$ ./assign0x03 5
5
```

This assignment asked up to over-write op code to do something. In this case, we want to return as the function when fib() is called. Dr. Jee gave us a pointer to the function, fib(). So, we basically can dereference it and use it as array to overwrite the current opcode.

So, how to get the opcode. We write a test function, test(), which we can disassemble to get the opcode for the return. The test function basically returns and does nothing else. So, that we can get the op code easily. From the objdump we can see the return opcode is "bx lr" and the hex is "1e ff 2f e1". 

So, since we have the opcode, we just need to overwrite the opcode of fib for the first 4 bytes, and we can do that in StartProfiling(). The over write is of the form of 4 byte because for ARM, the instruction length is 4 byte as it thumb instruction, and for ARM the length is fixed. 

StartProfiling
```
    func_ptr[0] = 0x1e;
    func_ptr[1] = 0xff;
    func_ptr[2] = 0x2f;
    func_ptr[3] = 0xe1;
```


The test function(`cat test.c`):
```
void test(){
    return;
}
```

The disassemble command and result (`objdump -D test | grep -A20 test:`):
```
00000000 test:
       0: 04 b0 2d e5                  	str	r11, [sp, #-4]!
       4: 00 b0 8d e2                  	add	r11, sp, #0
       8: 00 00 a0 e1                  	mov	r0, r0
       c: 00 d0 8b e2                  	add	sp, r11, #0
      10: 04 b0 9d e4                  	ldr	r11, [sp], #4
      14: 1e ff 2f e1                  	bx	lr
```

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
100003fb0: 55                          	pushq	%rbp
100003fb1: 48 89 e5                    	movq	%rsp, %rbp
100003fb4: 5d                          	popq	%rbp
100003fb5: c3                          	retq
```

## BONUS

**[Bonus]** You can gain bonus points for suggesting different instruction sequences semantically equivalent to return operation.

- You can suggest up to five instruction sequences for each architecture. 
   - 1pt for each sequence.
- For IA32, the length of instruction sequences should not exceed 5 bytes and for ARM, you can use up to two instructions (8 bytes).
   - The shorter, the better.

### IA-32

* cb
* c2
* ca
* jmp ret_address	
* call ret_offset

### ARM

1. b lr
2. mov pc, lr ; return to caller after the branch
3. stmfd SP!,{<registers>, LR}
4. ldmfd SP!,{<registers>, LR}
5. str RO, [R12], #4 ; push to stack
   str R14, [R12], #4 ; push the return addr
   bl R14; branch to R14 registers

  
## Part0x02: Callout and return for [IA32] (10 pt)

### IA-32

Compiling:
```
$ make
```

Running and Output:
```
$ ./assign0x03 5
addr func_ptr[5] = 0x8048a1f
addr retCallout  = 0x8048a52
addr retCallout(dest) - addr func_ptr[5](src)  = 33
inside return callout
134515230
```

This assignment is for IA-32 architecture. The issue here will be of length of opcode, as unlike ARM, the IA32 instruction set is not of constant length, specifically the op code instruction for "call" is of 5 byte length. In this case, we want to hijack fib() when it is called and pass the control to retCallout function. Dr. Jee gave us a pointer to the function, fib(). So, we basically can dereference it and use it as array to overwrite the current opcode.

So, how to get the opcode. We write a test function which we can disassemble to get the opcode for the return. The test function basically calls another function func1() and then returns. So, that we can get the op code easily and understand how the relative address is calculated. 

From the objdump we can see the call opcode is "callq" and the hex is "e8". But, using this resource (https://c9x.me/x86/html/file_module_x86_id_26.html), we can see that the "callq" opcode uses offset to call the destination address. Lets, use the test function to understand the offset calculation. Destination address for func1() is "0000000000000606 func1:". The current address is where the instruction pointer will be pointing to when "callq" is being executed. So, the current address is the address of  "callq" + 4 bytes, so it is "603: 90               	nop". The relative offset will calculated using this formula, "dest addr - current addr", so 606-603 = "03". Therefore, the "callq" should be called with "3" offset, if we want to call func1() function. So, the "callq" is of 5 byte long, and call instruction and offset account for 2 bytes. So, to make sure the instruction is correctly called, we will have to pad the last 3 bytes with "00". Thus, the complete instruction will be "e8 03 00 00 00". This is the same instruction that we can see in the objdump, "5fe: e8 03 00 00 00               	callq	3 <func1>". So, that is how we can use the call instruction and calculate the offset. 

So, since we have the opcode, but we just need to calculate the offset. After that we just need to overwrite the opcode of fib() for the first byte and put the offset in the next 4 bytes. We can do that in StartProfiling(). The offset will be calculated using this formulae, "(uint8_t)&retCallout - &func_ptr[5]". The destination address is (uint8_t)&retCallout. And, the current address will be &func_ptr[5], we are considering the address of the 6th byte because, thats where the IP will be pointing to after calling the "callq" OPCODE (1 byte of opcode and 4 bytes for offset). 

StartProfiling 
```
	// part B
    uint8_t *ret_ptr;
    ret_ptr = (uint8_t)&retCallout;

    uint8_t offset = ret_ptr - &func_ptr[5];
  	
  	func_ptr[0] = 0xe8; //call opcode
    func_ptr[1] = offset; // relative addr of retCallout
    func_ptr[2] = 0x00; // padding for the next 3 bytes
    func_ptr[3] = 0x00;
    func_ptr[4] = 0x00;
```


The test function(`cat test.c`):
```
void func1 (void);

void main(void)
{
   func1();
   return;
}

void func1(void)
{ 
	return;
}
```

The disassemble command and result (`objdump -D test | grep -A20 main:`):
```
00000000000005fa main:
     5fa: 55                           	pushq	%rbp
     5fb: 48 89 e5                     	movq	%rsp, %rbp
     5fe: e8 03 00 00 00               	callq	3 <func1>
     603: 90                           	nop
     604: 5d                           	popq	%rbp
     605: c3                           	retq

0000000000000606 func1:
     606: 55                           	pushq	%rbp
     607: 48 89 e5                     	movq	%rsp, %rbp
     60a: 90                           	nop
     60b: 5d                           	popq	%rbp
     60c: c3                           	retq
     60d: 0f 1f 00                     	nopl	(%rax)


```

