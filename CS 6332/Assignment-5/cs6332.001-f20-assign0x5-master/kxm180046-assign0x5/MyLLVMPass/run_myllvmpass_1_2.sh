#!/bin/sh

# project folder
# go to ~/tools/llvm/
# extact _.zip here

# TO COMPILE:
# run $ ./compile_myllvmpass.sh 
# OR
# copy Makefile from ~/tools/llvm/src/lib/Transforms/MyLLVMPass/Makefile
# to ~/tools/llvm/build/lib/Transforms/MyLLVMPass
# change dir to ~/tools/llvm/build/lib/Transforms/MyLLVMPass
# run $ make
# the compiled library loc: ~/tools/llvm/build/Release+Asserts/lib/MyLLVMPass.so

# TO RUN:
# ./run_myllvmpass.sh cs6332.001-f20-assign0x5-master/fib/fib.bc
# run $ opt -load ~/tools/llvm/build/Release+Asserts/lib/MyLLVMPass.so -MyLLVMPass  < _.bc > /dev/null

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
clang -S -emit-llvm -m32 cs6332.001-f20-assign0x5-master/fib/fib.c -o cs6332.001-f20-assign0x5-master/fib/fib.ll
opt -load ./build/Release+Asserts/lib/MyLLVMPass.so -MyLLVMPass3 -MyLLVMPass2  < ${var1} > ${var2}

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
clang -S -emit-llvm -m32 cs6332.001-f20-assign0x5-master/fib/fib.c -o cs6332.001-f20-assign0x5-master/fib/fib.ll
clang -S -emit-llvm -m32 cs6332.001-f20-assign0x5-master/fib/utils.c -o cs6332.001-f20-assign0x5-master/fib/utils.ll

opt -load ./build/Release+Asserts/lib/MyLLVMPass.so -MyLLVMPass4  -S < ${var1} >  cs6332.001-f20-assign0x5-master/fib/instFib.ll
llvm-link cs6332.001-f20-assign0x5-master/fib/instFib.ll cs6332.001-f20-assign0x5-master/fib/utils.ll -S -o ./cs6332.001-f20-assign0x5-master/fib/instDemo.ll
lli ./cs6332.001-f20-assign0x5-master/fib/instDemo.ll 9