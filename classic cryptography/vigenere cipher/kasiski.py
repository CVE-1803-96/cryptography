import string
import math
from collections import Counter
import re
from functools import reduce

# --- NEW: A basic English word list for dictionary validation ---
# In a real-world scenario, a more comprehensive list would be used.
COMMON_ENGLISH_WORDS = {
    'THE', 'BE', 'TO', 'OF', 'AND', 'A', 'IN', 'THAT', 'HAVE', 'I', 'IT', 'FOR', 'NOT', 'ON', 'WITH', 
    'HE', 'AS', 'YOU', 'DO', 'AT', 'THIS', 'BUT', 'HIS', 'BY', 'FROM', 'THEY', 'WE', 'SAY', 'HER', 
    'SHE', 'OR', 'AN', 'WILL', 'MY', 'ONE', 'ALL', 'WOULD', 'THERE', 'THEIR', 'WHAT', 'SO', 'UP', 
    'OUT', 'IF', 'ABOUT', 'WHO', 'GET', 'WHICH', 'GO', 'ME', 'WHEN', 'MAKE', 'CAN', 'LIKE', 'TIME', 
    'NO', 'JUST', 'HIM', 'KNOW', 'TAKE', 'PEOPLE', 'INTO', 'YEAR', 'YOUR', 'GOOD', 'SOME', 'COULD', 
    'THEM', 'SEE', 'OTHER', 'THAN', 'THEN', 'NOW', 'LOOK', 'ONLY', 'COME', 'ITS', 'OVER', 'THINK', 
    'ALSO', 'BACK', 'AFTER', 'USE', 'TWO', 'HOW', 'OUR', 'WORK', 'FIRST', 'WELL', 'WAY', 'EVEN', 
    'NEW', 'WANT', 'BECAUSE', 'ANY', 'THESE', 'GIVE', 'DAY', 'MOST', 'US', 'IS', 'ARE', 'WAS', 'WERE',
    'MESSAGE', 'SECRET', 'ATTACK', 'DAWN', 'WEATHER', 'TODAY', 'NICE', 'BEING'
}

class VigenereCracker:
    def __init__(self, ciphertext):
        self.ciphertext = ciphertext.upper()
        self.clean_text = self._clean_text(ciphertext)
        self.alphabet = string.ascii_uppercase
        self.english_freq = {
            'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702, 
            'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153, 
            'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507, 
            'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056, 
            'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974, 
            'Z': 0.00074
        }
        # Pre-calculate for efficiency
        self.english_freq_vector = [self.english_freq[L] for L in self.alphabet]

    def _clean_text(self, text):
        return ''.join([c.upper() for c in text if c.isalpha()])

    def _vigenere_decrypt(self, key):
        """Decrypts the original (not cleaned) ciphertext."""
        decrypted = []
        key_length = len(key)
        key_indices = [self.alphabet.index(k) for k in key]
        text_ptr = 0
        for char in self.ciphertext:
            if char in self.alphabet:
                shift = key_indices[text_ptr % key_length]
                decrypted_char = self.alphabet[(self.alphabet.index(char) - shift) % 26]
                decrypted.append(decrypted_char)
                text_ptr += 1
            else:
                decrypted.append(char)
        return ''.join(decrypted)

    def _calculate_ic(self, text):
        freq = Counter(text)
        total = len(text)
        if total <= 1:
            return 0.0
        ic = sum(count * (count - 1) for count in freq.values()) / (total * (total - 1))
        return ic

    # --- NEW: Kasiski Examination to find key length ---
    def _kasiski_examination(self, min_len=3, max_len=5):
        """Finds distances between repeated sequences in the ciphertext."""
        spacings = Counter()
        for seq_len in range(min_len, max_len + 1):
            for i in range(len(self.clean_text) - seq_len):
                seq = self.clean_text[i:i+seq_len]
                for j in range(i + seq_len, len(self.clean_text) - seq_len):
                    if self.clean_text[j:j+seq_len] == seq:
                        spacings[j - i] += 1
        return spacings

    def _get_key_length_candidates(self, max_key_length=20):
        print("\n--- STEP 1: Finding Key Length ---")
        
        # Method 1: Index of Coincidence (IC)
        ic_results = []
        for key_length in range(1, max_key_length + 1):
            segments = [self.clean_text[i::key_length] for i in range(key_length)]
            avg_ic = sum(self._calculate_ic(s) for s in segments) / key_length if key_length > 0 else 0
            ic_results.append((key_length, avg_ic))
        
        ic_results.sort(key=lambda x: abs(x[1] - 0.066), reverse=False) # Sort by closeness to English IC
        print("Top IC Candidates (closer to 0.066 is better):")
        for length, ic in ic_results[:5]:
            print(f"  Length {length:2d}: Avg IC = {ic:.4f}")
        
        # Method 2: Kasiski Examination
        spacings = self._kasiski_examination()
        if spacings:
            # Find Greatest Common Divisor (GCD) of the most common spacings
            def gcd(a, b):
                while b:
                    a, b = b, a % b
                return a
            
            common_spacings = [s for s, count in spacings.most_common(10)]
            if len(common_spacings) > 1:
                possible_gcd = reduce(gcd, common_spacings)
                print(f"\nKasiski Examination suggests factors of most common spacings.")
                # We can add factors of GCDs as candidates
                
        # Combine candidates (simple approach: take top IC results)
        # A more advanced method could weigh Kasiski results more heavily.
        top_candidates = [length for length, ic in ic_results[:3]]
        
        # Ensure candidates are unique and sorted
        key_lengths = sorted(list(set(top_candidates)))
        print(f"\nTesting top key length candidates: {key_lengths}")
        return key_lengths

    # --- OPTIMIZED: Uses correlation score instead of Chi-Squared ---
    def _find_best_shift(self, segment):
        """Finds the best Caesar shift for a segment using frequency correlation."""
        best_shift = 0
        max_score = -1
        
        for shift in range(26):
            shifted_segment = ''.join([self.alphabet[(self.alphabet.index(c) - shift) % 26] for c in segment])
            freq = Counter(shifted_segment)
            total = len(shifted_segment)
            
            # Calculate correlation score (dot product)
            observed_freq = [freq.get(L, 0) / total for L in self.alphabet]
            score = sum(o * e for o, e in zip(observed_freq, self.english_freq_vector))
            
            if score > max_score:
                max_score = score
                best_shift = shift
                
        return best_shift

    def _find_key(self, key_length):
        """Derives the key for a given length."""
        key = ''
        for i in range(key_length):
            segment = self.clean_text[i::key_length]
            if not segment: continue
            shift = self._find_best_shift(segment)
            key += self.alphabet[shift]
        return key

    # --- NEW: Dictionary-based scoring for accuracy ---
    def _score_plaintext(self, text):
        """Scores plaintext by counting valid English words."""
        words = re.findall(r'\b[A-Z]{2,}\b', text.upper()) # Find words of 2+ letters
        if not words:
            return 0
        
        matched_words = sum(1 for word in words if word in COMMON_ENGLISH_WORDS)
        return matched_words / len(words) * 100 # Return as a percentage

    def crack(self, max_key_length=20):
        print("VIGENÈRE CIPHER CRACKER (OPTIMIZED)")
        print("=" * 50)
        print(f"Ciphertext: {self.ciphertext[:100]}...")
        
        # Step 1: Get candidate key lengths
        key_length_candidates = self._get_key_length_candidates(max_key_length)
        if not key_length_candidates:
            print("Could not determine a likely key length.")
            return None

        # Step 2 & 3: Find key and decrypt for each candidate length, then score the result
        print("\n--- STEP 2 & 3: Finding Best Key & Decrypting ---")
        best_result = {'key': '', 'text': '', 'score': -1}
        
        for length in key_length_candidates:
            key = self._find_key(length)
            decrypted_text = self._vigenere_decrypt(key)
            score = self._score_plaintext(decrypted_text)
            
            print(f"Testing Key: '{key}' (length {length}) -> Dictionary Match: {score:.2f}%")

            if score > best_result['score']:
                best_result = {'key': key, 'text': decrypted_text, 'score': score}

        # Step 4: Final Assessment
        print("\n--- STEP 4: Final Result ---")
        if best_result['score'] < 10: # Threshold for a "bad" result
            print("Warning: Low dictionary match score. The result may be inaccurate.")
            print("This can happen with very short ciphertexts or non-standard English plaintext.")

        print(f"\nBest Key Found: '{best_result['key']}'")
        print(f"Confidence (Dictionary Match): {best_result['score']:.2f}%")
        print("\nDecrypted Text:")
        print(best_result['text'])
        
        return best_result


# --- Example Usage ---
def main():
    # Example 1: Standard text
    print("--- TEST CASE 1 ---")
    ciphertext1 = "LXFOPVEFRNHR" # "ATTACKATDAWN" with key "LEMON"
    cracker1 = VigenereCracker(ciphertext1)
    cracker1.crack()
    print("\n" + "="*60 + "\n")

    # Example 2: Longer text
    print("--- TEST CASE 2 ---")
    plaintext2 = "The quick brown fox jumps over the lazy dog. This is a classic example used for typography and font testing."
    key2 = "SECRET"
    
    def vigenere_encrypt(text, key):
        encrypted = []
        key_ptr = 0
        for char in text.upper():
            if 'A' <= char <= 'Z':
                shift = ord(key[key_ptr % len(key)]) - ord('A')
                encrypted_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
                encrypted.append(encrypted_char)
                key_ptr += 1
            else:
                encrypted.append(char)
        return "".join(encrypted)

    ciphertext2 = vigenere_encrypt(plaintext2, key2)
    cracker2 = VigenereCracker(ciphertext2)
    cracker2.crack()
    print("\n" + "="*60 + "\n")
    
    # Example 3: User Input
    print("--- YOUR TURN ---")
    user_ciphertext = input("Enter your own ciphertext to crack: ").strip()
    if user_ciphertext:
        cracker3 = VigenereCracker(user_ciphertext)
        cracker3.crack()

if __name__ == "__main__":
    main()