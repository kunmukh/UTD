CFLAGS += -g -m32  -mpreferred-stack-boundary=2 -fno-stack-protector -no-pie -fno-pic -I../include
GCCVERSIONGTEQ8 := $(shell expr `gcc -dumpversion | cut -f1 -d.` \>= 8)

ifeq "$(GCCVERSIONGTEQ8)" "1"
	CFLAGS += -fcf-protection=none
endif

OBJDUMP = objdump
OBJS = ia32_disas.o

.PHONY = all objs clean

all: assign0x04

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

assign0x04: assign0x04.c ia32_callout.S fib.o ia32_disas.o
	$(CC) $(CFLAGS)  $^ -static -Wl,-N -o $@
	$(OBJDUMP) -d $@ > $@.dis

objs: $(OBJS)

clean:
	rm -f assign0x04 *.o *.dis 
