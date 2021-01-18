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
# partC
# in cs6332.001-f20-assign0x5-master/db_connector
# make
# $ ./run_myllvmpass.sh cs6332.001-f20-assign0x5-master/db_connector/db_connector.ll
echo "=================PART3================="
clang -S -emit-llvm -m32 cs6332.001-f20-assign0x5-master/db_connector/utils.c -o cs6332.001-f20-assign0x5-master/db_connector/utils.ll

opt -load ./build/Release+Asserts/lib/MyLLVMPass.so -MyLLVMPass5  -S < ${var1} >  cs6332.001-f20-assign0x5-master/db_connector/instDB.ll
llvm-link cs6332.001-f20-assign0x5-master/db_connector/instDB.ll cs6332.001-f20-assign0x5-master/db_connector/utils.ll -S -o ./cs6332.001-f20-assign0x5-master/db_connector/instDemo.ll
lli ./cs6332.001-f20-assign0x5-master/db_connector/instDemo.ll
