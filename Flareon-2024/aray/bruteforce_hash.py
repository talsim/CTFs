import hashlib

# Target SHA-256 hash to crack
target_hash = '403d5f23d149670348b147a15eeb7010914701a7e99aad2e43f90cfa0325c76f'

# Loop through all possible 2-byte combinations
for b1 in range(256):  # First byte (0x00 to 0xff)
    for b2 in range(256):  # Second byte (0x00 to 0xff)
        # Create the 2-byte string
        byte_string = bytes([b1, b2])
        # Calculate SHA-256 hash
        hash_value = hashlib.sha256(byte_string).hexdigest()
        
        # Check if it matches the target hash
        if hash_value == target_hash:
            print(f"Found: {byte_string} -> {hash_value}")
