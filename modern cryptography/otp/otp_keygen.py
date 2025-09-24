import os

key_path = "key.bin"  # binary file is safer for raw bytes
key_bytes = os.urandom(24)
with open(key_path, "wb") as f:
    f.write(key_bytes)

print(f"Saved {key_path} with {len(key_bytes)} bytes.")
