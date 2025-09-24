import sys
import os

def read_binary_file(filename):
    """Read binary file and return bytes"""
    with open(filename, "rb") as f:
        return f.read()

def write_binary_file(filename, data):
    """Write binary data to file"""
    with open(filename, "wb") as f:
        f.write(data)

def read_key_file(filename):
    """Read key file as binary"""
    with open(filename, "rb") as f:
        return f.read()

def otp_xor_bytes(message_bytes, key_bytes):
    """Perform XOR operation on bytes"""
    return bytes([m ^ k for m, k in zip(message_bytes, key_bytes)])

def bytes_to_display_string(data, max_display=50):
    """Convert bytes to a display-friendly string representation"""
    if len(data) <= max_display:
       
        return ''.join([f'\\x{b:02x}' for b in data])
    else:
        
        truncated = data[:max_display]
        return ''.join([f'\\x{b:02x}' for b in truncated]) + "..."

def bytes_to_ascii_safe_string(data, max_display=50):
    """Convert bytes to ASCII-safe string representation"""
    result = []
    for b in data[:max_display]:
        if 32 <= b <= 126:  
            result.append(chr(b))
        else:
            result.append(f'\\x{b:02x}')
    
    display_str = ''.join(result)
    if len(data) > max_display:
        display_str += "..."
    return display_str

def main():
   
    if not os.path.exists("in.bin"):
        print("Error: in.bin file not found!")
        sys.exit(1)
    
    if not os.path.exists("key.bin"):
        print("Error: key.bin file not found!")
        sys.exit(1)


    message_bytes = read_binary_file("in.bin")
    key_bytes = read_key_file("key.bin")

   
    if len(key_bytes) != len(message_bytes):
        print("Error: key length must match message length in bytes!")
        print(f"Message length: {len(message_bytes)} bytes")
        print(f"Key length: {len(key_bytes)} bytes")
        sys.exit(1)

 
    mode = input("Do you want to (E)ncrypt or (D)ecrypt? ").strip().lower()

   
    print("\n" + "="*60)
    print("OPERATION DETAILS:")
    print("="*60)
    
    if mode.startswith("e"):
        print("Mode: Encryption")
        print(f"Plaintext size: {len(message_bytes)} bytes")
        print(f"Plaintext (hex): {bytes_to_display_string(message_bytes)}")
        print(f"Plaintext (ASCII-safe): {bytes_to_ascii_safe_string(message_bytes)}")
    elif mode.startswith("d"):
        print("Mode: Decryption") 
        print(f"Ciphertext size: {len(message_bytes)} bytes")
        print(f"Ciphertext (hex): {bytes_to_display_string(message_bytes)}")
        print(f"Ciphertext (ASCII-safe): {bytes_to_ascii_safe_string(message_bytes)}")
    else:
        print("Invalid choice. Please select E or D.")
        sys.exit(1)
    
    print(f"Key size: {len(key_bytes)} bytes")
    print(f"Key (hex): {bytes_to_display_string(key_bytes)}")
    print(f"Key (ASCII-safe): {bytes_to_ascii_safe_string(key_bytes)}")


    result_bytes = otp_xor_bytes(message_bytes, key_bytes)

    
    print("\n" + "="*60)
    print("RESULT:")
    print("="*60)
    
    if mode.startswith("e"):
        print("Ciphertext generated:")
        print(f"Ciphertext (hex): {bytes_to_display_string(result_bytes)}")
        print(f"Ciphertext (ASCII-safe): {bytes_to_ascii_safe_string(result_bytes)}")
    elif mode.startswith("d"):
        print("Plaintext recovered:")
        print(f"Plaintext (hex): {bytes_to_display_string(result_bytes)}")
        print(f"Plaintext (ASCII-safe): {bytes_to_ascii_safe_string(result_bytes)}")
        
        
        try:
            decoded_text = result_bytes.decode('utf-8')
            if len(decoded_text) <= 100:
                print(f"Plaintext (UTF-8 decoded): {decoded_text}")
            else:
                print(f"Plaintext (UTF-8 decoded, truncated): {decoded_text[:100]}...")
        except UnicodeDecodeError:
            print("Plaintext (UTF-8): [Contains non-UTF-8 data]")

    
    write_binary_file("in.bin", result_bytes)

    print(f"\nOperation complete. Result written to in.bin")
    print(f"Result size: {len(result_bytes)} bytes")

if __name__ == "__main__":
    main()