# Assignment 0x03 (20 pt)

In this homework you will exercise a basic binary/code patching to build foundation for later tasks of  profiling the execution of a function using binary patching and writing a code for the basic x86/ARM disassembly. The homework provide skeleton codes for [i386 (or IA32)][IA32] and [ARM] architectures.

## How to submit your work
This assignment will be **due on 11:59 PM, October 30**. 

Please create a folder with `<netid>-assign0x03` with the following structure to submit the assignment.
You will extend the provided skeleton codes to complete each part. Each folder will contain the necessary source files to reproduce your work. Please do not forget to write a README.md document to describe your solution. After completing the assignment, compress the folder and submit the file to eLearning.

```
<netid>-assign0x03/
├── part0x01-arm/
├── part0x01-ia32/
├── part0x02/
├── part0x03/
└── README.md
```

## Part0x01: Patching binary to return (10 pt + bonus 10pt)

The first step will get you warmed-up and comfortable with patching code. Look at the bottom of main(). Just before *main* calls *fib()* it calls *StartProfiling*. *StartProfiling* is your hook. It gives you and opportunity to inspect and/or modify the target function, *fib()* in this case, before it starts executing. Your objective in Part1 is to use StartProfiling to binary patch *fib()* to *immediately return*. 

Although this may sound pointless, this technique is very useful in the real world. Often you have debugging code that needs to be removed after some time. On-the-fly binary patching allows you to remove functionality without recompiling your code. If *fib()* was some debugging code and this was in the kernel, binary patching fib() to return immediately would allow you to speed up the kernel without rebooting the machine.

You will first add the patching instructions for [IA32] (5 pt) and for [ARM] (5 pt).

**[Bonus]** You can gain bonus points for suggesting different instruction sequences semantically equivalent to return operation.

- You can suggest up to five instruction sequences for each architecture. 
   - 1pt for each sequence.
- For IA32, the length of instruction sequences should not exceed 5 bytes and for ARM, you can use up to two instructions (8 bytes).
   - The shorter, the better. 
  
## Part0x02: Callout and return for [IA32] (10 pt)

In this step you should accomplish the same thing as Part0x01 but this time using [a callout][glue-IA32] that emulates function return. The trickiness about  is that they need to save all the registers and condition registers (EFLAGS for Intel) because the code was not expecting a callout. The normal gcc calling conventions don't work. Find the glue code in [ia32_callout.S][glue-IA32].

You should patch the first instruction on fib() with a callout. The callout should emulate the behavior of the function return behavior by returning not to the calling site of the callout (which is the normal behavior) but directly to the return PC on the stack.

[Hint] You will patch *fib()* to call [glue code][glue-IA32]. What is the format for 'call' instruction?

Try to add and run an aritrary code from the callout context by replacing *NOT_IMPLEMENTED()* inside *handleRetCallout()* with something else.

## Part0x03: Callout and return for [ARM] (bonus 10 pt)

This time, you will implement the same binary patching for [ARM]. However, we do not provide you glue code to emulate function return behavior. Write your own glue code to implement.

[IA32]:assign0x03-ia32
[ARM]:assign0x03-arm
[glue-IA32]:assign0x03-ia32/ia32_callout.S



