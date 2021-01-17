CC=gcc
CFLAGS += -g -fno-stack-protector -no-pie -fno-pic
OBJDUMP = objdump
OBJS = ia32_disas.o

.PHONY = all objs clean


%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

assign0x03: assign0x03.c arm_callout.S
	$(CC) $(CFLAGS)  $^ -static -Wl,-N -o $@
	$(OBJDUMP) -d $@ > $@.dis

objs: $(OBJS)

clean:
	rm -f assign0x03 *.o *.dis 
