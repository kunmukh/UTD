CLANG=$(shell which clang)
DIS=$(shell which llvm-dis)
CFLAGS+=-m32

.PHONY: all diff clean

all: db_connector

%.o: %.c
	$(CLANG) $(CFLAGS) -c -o $@ $<

%.ll:%.c
	$(CLANG) $(CFLAGS) -c -emit-llvm -o $(basename $<).bc $<
	opt -O1  $(basename $<).bc > $(basename $<)_O1.bc

	opt -dot-cfg $(basename $<).bc > /dev/null
	dot -Tpdf cfg.main.dot >  $(basename $<).pdf

	opt -dot-cfg $(basename $<)_O1.bc > /dev/null
	dot -Tpdf cfg.main.dot >  $(basename $<)_O1.pdf

	$(DIS) $(basename $<).bc
	$(DIS) $(basename $<)_O1.bc


libutils.so: utils.o
	$(CLANG) -shared -fpic -o $@ $<

db_connector: db_connector.ll utils.o
	$(CLANG) $(CFLAGS) $< utils.o -o $@

db_connector_O1: db_connector_O1.ll utils.o
	$(CLANG) $(CFLAGS) $< utils.o -o $@

diff: db_connector.ll
	opt -S -load ${LLVM_LIB}/MyLLVMPass.so -MyLLVMPass < $< > $(basename $<)_opt.ll

clean:
	rm -f *.ll *.bc *.o db_connector *.dot *.pdf *.cpp

