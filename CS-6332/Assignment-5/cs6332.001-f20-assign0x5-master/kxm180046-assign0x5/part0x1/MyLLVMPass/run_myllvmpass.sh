#!/bin/sh

var1=$1
var2="/dev/null"
if [ "$#" -ne 1 ]
then
	echo "USAGE: ./run_myllvmpass.sh [FIB INPUT BC/LL FILE]"
	exit 1
fi

#******
# partA
# in cs6332.001-f20-assign0x5-master/fib/make clean
# $ make
# $ clang -S -emit-llvm -m32 fib.c

# $ ./run_myllvmpass.sh cs6332.001-f20-assign0x5-master/fib/fib.ll
echo "=================PART1================="
clang -S -emit-llvm -m32 kxm180046-assign0x5/part0x1/fib/fib.c -o kxm180046-assign0x5/part0x1/fib/fib.ll
opt -load ./build/Release+Asserts/lib/MyLLVMPass.so -MyLLVMPass3 -MyLLVMPass2  < ${var1} > ${var2}