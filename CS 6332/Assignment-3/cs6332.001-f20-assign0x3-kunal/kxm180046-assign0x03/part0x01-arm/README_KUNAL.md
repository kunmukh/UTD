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
