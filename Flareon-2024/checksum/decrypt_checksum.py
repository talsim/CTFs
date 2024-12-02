import base64

# Decoding the base64 encoded string in main_a func
encoded_str = "cQoFRQErX1YAVw1zVQdFUSxfAQNRBXUNAxBSe15QCVRVJ1pQEwd/WFBUAlElCFBFUnlaB1ULByRdBEFdfVtWVA=="
decoded_str = base64.b64decode(encoded_str)

# Hardcoded XOR key in main_a
xor_key = "FlareOn2024"  # Extracted the key from the binary

# Perform XOR to reverse the operation and find the correct checksum
checksum = ''.join(chr(byte ^ ord(xor_key[i % len(xor_key)])) for i, byte in enumerate(decoded_str))

print("Correct checksum: ", checksum)
