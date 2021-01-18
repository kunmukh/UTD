CFLAGS += -g -fno-stack-protector -no-pie -fno-pic -I ../include
OBJDUMP = objdump
OBJS = ia32_disas.o

.PHONY = all objs clean
all: assign0x04

%.o: %.S
	$(CC) $(CFLAGS) -c -o $@ $<

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

assign0x04: assign0x04.c arm_callout.S fib.o
	$(CC) $(CFLAGS)  $^ -static -Wl,-N -o $@
	$(OBJDUMP) -d $@ > $@.dis

objs: $(OBJS)

clean:
	rm -f assign0x04 *.o *.dis 
