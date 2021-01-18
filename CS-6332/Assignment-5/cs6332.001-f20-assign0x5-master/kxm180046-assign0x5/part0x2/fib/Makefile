CFLAGS += -g -m32

CLANG=$(shell which clang)
DIS=$(shell which llvm-dis)
OPT=$(shell which OPT)

OBJDUMP = objdump

.PHONY = all clean

fib: fib.c utils.o
	$(CC) $(CFLAGS)  $^ -static -Wl,-N -o $@
	$(OBJDUMP) -d $@ > $@.dis

%.o: %.c
	$(CLANG) $(CFLAGS) -c -o $@ $<

%.ll:%.c
	$(CLANG) $(CFLAGS) -c -emit-llvm -o $(basename $<).bc $<
	$(DIS) $(basename $<).bc

diff: fib.ll
	opt -debug -S -load ${LLVM_LIB}/MyLLVMPass.so -MyLLVMPass < $< > $(basename $<)_opt.ll
	-diff $< $(basename $<)_opt.ll

clean:
	rm -f fib *.o *.dis *.s *.ll *.bc cfg.*
