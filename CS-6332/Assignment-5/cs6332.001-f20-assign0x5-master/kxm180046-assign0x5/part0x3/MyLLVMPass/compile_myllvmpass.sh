#!/bin/sh

cd ./build/lib/Transforms/MyLLVMPass
echo "-------------------------------------"

make

echo "-------------------------------------"

cd ../../../../

ls -l --color ./build/Release+Asserts/lib/MyLLVMPass.so
echo "-------------------------------------"
