#!/usr/bin/env python3
"""
Two Time Pad Attack Implementation
Cracks messages encrypted with the same one-time pad key
"""

import string
from collections import Counter
import itertools

class TwoTimePadAttack:
    def __init__(self):
        
        self.common_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her',
            'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how',
            'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did',
            'its', 'let', 'put', 'say', 'she', 'too', 'use', 'that', 'with', 'have',
            'this', 'will', 'your', 'from', 'they', 'know', 'want', 'been', 'good',
            'much', 'some', 'time', 'very', 'when', 'come', 'here', 'just', 'like',
            'long', 'make', 'many', 'over', 'such', 'take', 'than', 'them', 'well',
            'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why',
            'will', 'with', 'would', 'your', 'about', 'above', 'after', 'again',
            'against', 'among', 'around', 'because', 'before', 'below', 'between',
            'during', 'except', 'into', 'through', 'under', 'until', 'upon',
            'within', 'without'
        }
        
        # English letter frequency (space is most common)
        self.english_freq = {
            ' ': 18.0, 'e': 12.7, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7.0, 'n': 6.7,
            's': 6.3, 'h': 6.1, 'r': 6.0, 'd': 4.3, 'l': 4.0, 'c': 2.8, 'u': 2.8,
            'm': 2.4, 'w': 2.4, 'f': 2.2, 'g': 2.0, 'y': 2.0, 'p': 1.9, 'b': 1.5,
            'v': 1.0, 'k': 0.8, 'j': 0.15, 'x': 0.15, 'q': 0.10, 'z': 0.07
        }
    
    def hex_to_bytes(self, hex_string):
        """Convert hex string to bytes"""
        return bytes.fromhex(hex_string)
    
    def bytes_to_hex(self, byte_data):
        """Convert bytes to hex string"""
        return byte_data.hex()
    
    def xor_bytes(self, a, b):
        """XOR two byte strings"""
        return bytes([x ^ y for x, y in zip(a, b)])
    
    def is_printable(self, text):
        """Check if text contains mostly printable characters"""
        if not text:
            return False
        
        printable_count = sum(1 for c in text if 32 <= c <= 126)
        return printable_count / len(text) > 0.8
    
    def english_score(self, text):
        """Score how English-like the text is"""
        if not text:
            return 0
        
      
        try:
            text_str = text.decode('latin-1').lower()
        except:
            return 0
        
        score = 0
        total_chars = len(text_str)
        
        if total_chars == 0:
            return 0
        
       
        for char in text_str:
            if char in self.english_freq:
                score += self.english_freq[char]
        
       
        words = text_str.split()
        common_word_count = sum(1 for word in words if word.lower() in self.common_words)
        score += common_word_count * 10
        
        return score / total_chars if total_chars > 0 else 0
    
    def crack_single_byte_xor(self, ciphertext):
        """Attempt to crack single-byte XOR encryption"""
        best_score = 0
        best_key = 0
        best_plaintext = b''
        
        for key in range(256):
            plaintext = bytes([b ^ key for b in ciphertext])
            score = self.english_score(plaintext)
            
            if score > best_score:
                best_score = score
                best_key = key
                best_plaintext = plaintext
        
        return best_key, best_plaintext, best_score
    
    def two_time_pad_attack(self, ciphertext1, ciphertext2):
        """
        Perform two-time pad attack on two ciphertexts encrypted with the same key
        """
        
        message_xor = self.xor_bytes(ciphertext1, ciphertext2)
        
       
        recovered_msg1 = bytearray(len(message_xor))
        recovered_msg2 = bytearray(len(message_xor))
        
        
        confidence = [0] * len(message_xor)
        
        
        for i in range(len(message_xor)):
            # If we XOR with space (0x20), we might get a letter
            potential_char = message_xor[i] ^ 0x20
            

            if 32 <= potential_char <= 126:
               
                option1_msg1 = 0x20
                option1_msg2 = potential_char
                
               
                option2_msg1 = potential_char
                option2_msg2 = 0x20
                

                recovered_msg1[i] = option2_msg1  # Default to option B
                recovered_msg2[i] = option2_msg2
                confidence[i] = 1
        

        
        return bytes(recovered_msg1), bytes(recovered_msg2), confidence
    
    def crib_drag(self, ciphertext1, ciphertext2, crib):
        """
        Use crib dragging to find known plaintext in the messages
        """
        message_xor = self.xor_bytes(ciphertext1, ciphertext2)
        crib_bytes = crib.encode()
        
        positions = []
        
        
        for i in range(len(message_xor) - len(crib_bytes) + 1):
            
            potential = self.xor_bytes(crib_bytes, message_xor[i:i+len(crib_bytes)])
            
            
            if self.is_printable(potential) and self.english_score(potential) > 5:
                positions.append((i, crib, potential.decode('latin-1')))
        
        return positions
    
    def advanced_attack(self, ciphertexts):
        """
        Advanced attack that can handle multiple ciphertexts encrypted with the same key
        """
        if len(ciphertexts) < 2:
            raise ValueError("Need at least 2 ciphertexts for two-time pad attack")
        
        
        min_len = min(len(c) for c in ciphertexts)
        
        
        truncated_ctexts = [c[:min_len] for c in ciphertexts]
        
        # The key insight: c1 ⊕ c2 = m1 ⊕ m2
        # If we have multiple pairs, we can get more constraints
        
        recovered_messages = [bytearray(min_len) for _ in range(len(ciphertexts))]
        confidence = [[0] * min_len for _ in range(len(ciphertexts))]
        
        
        for pos in range(min_len):
            ct_bytes = [c[pos] for c in truncated_ctexts]
            
            
            best_key = 0
            best_score = -1
            
            for key_byte in range(256):
               
                potential_chars = [key_byte ^ ct for ct in ct_bytes]
                
                
                score = 0
                for char in potential_chars:
                    char_str = chr(char) if 32 <= char <= 126 else ''
                    if char_str.lower() in self.english_freq:
                        score += self.english_freq[char_str.lower()]
                
                if score > best_score:
                    best_score = score
                    best_key = key_byte
            
            
            if best_score > 5:
                for i in range(len(ciphertexts)):
                    recovered_messages[i][pos] = best_key ^ ct_bytes[i]
                    confidence[i][pos] = 1
        
        return [bytes(msg) for msg in recovered_messages], confidence
    
    def interactive_attack(self, ciphertext1, ciphertext2):
        """
        Interactive attack that allows user to provide known plaintext hints
        """
        print("Interactive Two-Time Pad Attack")
        print("=" * 50)
        
        message_xor = self.xor_bytes(ciphertext1, ciphertext2)
        min_len = min(len(ciphertext1), len(ciphertext2))
        
        recovered_msg1 = bytearray(min_len)
        recovered_msg2 = bytearray(min_len)
        
        
        for i in range(min_len):
            
            potential_msg2 = message_xor[i] ^ 0x20
            if 32 <= potential_msg2 <= 126:
                recovered_msg1[i] = 0x20
                recovered_msg2[i] = potential_msg2
            else:
                
                potential_msg1 = message_xor[i] ^ 0x20
                if 32 <= potential_msg1 <= 126:
                    recovered_msg1[i] = potential_msg1
                    recovered_msg2[i] = 0x20
                else:
                    
                    recovered_msg1[i] = ord('?')
                    recovered_msg2[i] = ord('?')
        
        while True:
            print("\nCurrent Recovery:")
            print(f"Message 1: {recovered_msg1.decode('latin-1', errors='replace')}")
            print(f"Message 2: {recovered_msg2.decode('latin-1', errors='replace')}")
            
            print("\nOptions:")
            print("1. Provide known plaintext (crib)")
            print("2. Manually edit a character")
            print("3. Auto-refine using English frequency")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                crib = input("Enter known plaintext: ").strip()
                positions = self.crib_drag(ciphertext1, ciphertext2, crib)
                
                if positions:
                    print(f"\nFound {len(positions)} possible positions:")
                    for i, (pos, crib_text, potential) in enumerate(positions):
                        print(f"{i+1}. Position {pos}: '{crib_text}' -> '{potential}'")
                    
                    if positions:
                        selection = input("Select position to apply (or 0 to cancel): ").strip()
                        if selection.isdigit() and 1 <= int(selection) <= len(positions):
                            pos, crib_text, potential = positions[int(selection)-1]
                            crib_bytes = crib_text.encode()
                            
                           
                            for j in range(len(crib_bytes)):
                                if pos + j < min_len:
                                    recovered_msg1[pos + j] = crib_bytes[j]
                                    recovered_msg2[pos + j] = ord(potential[j]) if j < len(potential) else ord('?')
                else:
                    print("No matches found for that crib.")
            
            elif choice == '2':
                msg_num = input("Edit message 1 or 2? (1/2): ").strip()
                pos = input("Position to edit: ").strip()
                char = input("New character: ").strip()
                
                if msg_num in ['1', '2'] and pos.isdigit() and char:
                    pos_int = int(pos)
                    if 0 <= pos_int < min_len:
                        if msg_num == '1':
                            recovered_msg1[pos_int] = ord(char[0])
                            
                            if pos_int < len(message_xor):
                                recovered_msg2[pos_int] = message_xor[pos_int] ^ recovered_msg1[pos_int]
                        else:
                            recovered_msg2[pos_int] = ord(char[0])
                            
                            if pos_int < len(message_xor):
                                recovered_msg1[pos_int] = message_xor[pos_int] ^ recovered_msg2[pos_int]
            
            elif choice == '3':
                
                for i in range(min_len):
                    if recovered_msg1[i] == ord('?') or recovered_msg2[i] == ord('?'):
                        
                        best_score = -1
                        best_pair = (ord('?'), ord('?'))
                        
                        for c1 in range(32, 127):  
                            c2 = message_xor[i] ^ c1 if i < len(message_xor) else ord('?')
                            
                            if 32 <= c2 <= 126:
                                
                                score = self.english_freq.get(chr(c1).lower(), 0) + \
                                       self.english_freq.get(chr(c2).lower(), 0)
                                
                                if score > best_score:
                                    best_score = score
                                    best_pair = (c1, c2)
                        
                        if best_score > 0:
                            recovered_msg1[i], recovered_msg2[i] = best_pair
            
            elif choice == '4':
                break
        
        return bytes(recovered_msg1), bytes(recovered_msg2)


def demo_attack():
    """Demonstrate the two-time pad attack"""
    attack = TwoTimePadAttack()
    
    
    message1 = "The quick brown fox jumps over the lazy dog"
    message2 = "Two time pad attack demonstration works"
    
    
    max_len = max(len(message1), len(message2))
    key = b'\x2a\x7f\x13\x45\x89\xab\xcd\xef\x12\x34\x56\x78\x9a\xbc\xde\xf0' * (max_len // 16 + 1)
    key = key[:max_len]
    
    
    ciphertext1 = attack.xor_bytes(message1.encode(), key)
    ciphertext2 = attack.xor_bytes(message2.encode(), key)
    
    print("Two-Time Pad Attack Demonstration")
    print("=" * 50)
    print(f"Message 1: {message1}")
    print(f"Message 2: {message2}")
    print(f"Key (hex): {key.hex()}")
    print(f"Ciphertext 1 (hex): {ciphertext1.hex()}")
    print(f"Ciphertext 2 (hex): {ciphertext2.hex()}")
    print("\n" + "=" * 50)
    
    
    print("\nPerforming two-time pad attack...")
    recovered1, recovered2, confidence = attack.two_time_pad_attack(ciphertext1, ciphertext2)
    
    print(f"Recovered Message 1: {recovered1.decode('latin-1', errors='replace')}")
    print(f"Recovered Message 2: {recovered2.decode('latin-1', errors='replace')}")
    
   
    print("\nTrying crib dragging with common words...")
    cribs = ['the', 'and', 'attack', 'quick', 'brown', 'lazy', 'dog', 'time', 'pad']
    
    for crib in cribs:
        positions = attack.crib_drag(ciphertext1, ciphertext2, crib)
        if positions:
            print(f"Crib '{crib}' found at positions: {[p[0] for p in positions]}")
    
   
    print("\nStarting interactive attack...")
    final1, final2 = attack.interactive_attack(ciphertext1, ciphertext2)
    
    print("\nFinal Results:")
    print(f"Message 1: {final1.decode('latin-1', errors='replace')}")
    print(f"Message 2: {final2.decode('latin-1', errors='replace')}")
    

    original1 = message1.encode()
    original2 = message2.encode()
    
    min_len = min(len(original1), len(final1))
    accuracy1 = sum(1 for i in range(min_len) if original1[i] == final1[i]) / min_len * 100
    
    min_len = min(len(original2), len(final2))
    accuracy2 = sum(1 for i in range(min_len) if original2[i] == final2[i]) / min_len * 100
    
    print(f"\nAccuracy: Message 1: {accuracy1:.1f}%, Message 2: {accuracy2:.1f}%")


if __name__ == "__main__":
    demo_attack()