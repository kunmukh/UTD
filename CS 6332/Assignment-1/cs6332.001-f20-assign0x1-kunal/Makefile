CC=gcc
CFLAGS=-g

all: part0 part1 part2 part3 part4 part5

part0: driver0.c memsets.c
	$(CC) $(CFLAGS) -o $@  $<
	@echo "===" $@ "==="
	./$@

part1: driver1.o memsets.o
	gcc -g -o part1 driver1.o memsets.o
	@echo "===" $@ "==="
	./part1

driver1.o: driver1.c
	gcc -g -std=c99 -c driver1.c

memsets.o: memsets.c memsets.h
	gcc -g -c memsets.c

part2: driver1.o libmemsets.a
	gcc -g -o part2 driver1.o libmemsets.a
	@echo "===" $@ "==="
	./part2

libmemsets.a: memsets.o
	ar rs libmemsets.a memsets.o

part3: driver1.o libmemsets.so
	gcc -g -o part3 driver1.o libmemsets.so
	@echo "===" $@ "==="
	LD_LIBRARY_PATH=. ./part3 #linux
	# ./part3

libmemsets.so: memsets.o
	gcc -shared -o libmemsets.so memsets.o

part4: driver4.c libmemsets.so
	gcc -o part4 driver4.c -ldl
	@echo "===" $@ "==="
	./part4

part5: memsetinject.so part3exe
	@echo "===" $@ "==="
	LD_LIBRARY_PATH=. LD_PRELOAD=./memsetinject.so ./part3exe # Linux
	#LD_LIBRARY_PATH=. DYLD_INSERT_LIBRARIES=./memsetinject.so DYLD_FORCE_FLAT_NAMESPACE=1 ./part3exe # OS X

memsetinject.so: memsetinject.c
	gcc -shared -fPIC -o memsetinject.so memsetinject.c # Linux
	#gcc -shared -fPIC -o memsetinject.so memsetinject.c # OS X

part3exe: driver1.o libmemsets.so
	gcc -g -o part3exe driver1.o libmemsets.so

clean:
	rm -rf part? *.a *.o *.so *.dSYM part3exe

