#!/bin/sh

var1=$1
var2="/dev/null"
if [ "$#" -ne 1 ]
then
	echo "USAGE: ./run_myllvmpass.sh [FIB INPUT BC/LL FILE]"
	exit 1
fi

#******
# partB
# export FIB_LOGGER=1

# in cs6332.001-f20-assign0x5-master/fib/make clean
# $ make
# $ clang -S -emit-llvm -m32 fib.c
# $ clang -S -emit-llvm -m32 utils.c

# in ~/tools/llvm
# $ ./run_myllvmpass.sh cs6332.001-f20-assign0x5-master/fib/fib.ll
# to check: meld cs6332.001-f20-assign0x5-master/fib/instDemo.s cs6332.001-f20-assign0x5-master/fib/fib.s
echo "=================PART2================="
clang -S -emit-llvm -m32 kxm180046-assign0x5/part0x2/fib/fib.c -o kxm180046-assign0x5/part0x2/fib/fib.ll
clang -S -emit-llvm -m32 kxm180046-assign0x5/part0x2/fib/utils.c -o kxm180046-assign0x5/part0x2/fib/utils.ll

opt -load ./build/Release+Asserts/lib/MyLLVMPass.so -MyLLVMPass4  -S < ${var1} >  kxm180046-assign0x5/part0x2/fib/instFib.ll
llvm-link kxm180046-assign0x5/part0x2/fib/instFib.ll kxm180046-assign0x5/part0x2/fib/utils.ll -S -o ./kxm180046-assign0x5/part0x2/fib/instDemo.ll
lli ./kxm180046-assign0x5/part0x2/fib/instDemo.ll 9