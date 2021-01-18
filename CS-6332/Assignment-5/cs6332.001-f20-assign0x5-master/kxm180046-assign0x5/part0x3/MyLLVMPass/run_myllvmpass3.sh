#!/bin/sh

var1=$1
var2="/dev/null"
if [ "$#" -ne 1 ]
then
	echo "USAGE: ./run_myllvmpass.sh [FIB INPUT BC/LL FILE]"
	exit 1
fi

#******
# partC
# in kxm180046/part0x3/db_connector
# make
# $ ./run_myllvmpass.sh kxm180046/part0x3/db_connector/db_connector.ll
echo "=================PART3================="
clang -S -emit-llvm -m32 kxm180046/part0x3/db_connector/utils.c -o kxm180046/part0x3/db_connector/utils.ll

opt -load ./build/Release+Asserts/lib/MyLLVMPass.so -MyLLVMPass5  -S < ${var1} >  kxm180046/part0x3/db_connector/instDB.ll
llvm-link kxm180046/part0x3/db_connector/instDB.ll kxm180046/part0x3/db_connector/utils.ll -S -o ./kxm180046/part0x3/db_connector/instDemo.ll
lli ./kxm180046/part0x3/db_connector/instDemo.ll
