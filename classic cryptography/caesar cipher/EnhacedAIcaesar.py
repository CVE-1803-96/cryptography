from langdetect import detect, DetectorFactory
import re

# For consistent results
DetectorFactory.seed = 0

ALPHABET = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def detect_language(text):
    """Detect the language of the text using langdetect"""
    # Clean the text - remove non-alphabetic characters except spaces
    cleaned_text = re.sub(r'[^A-Za-z\s]', '', text)
    
    if len(cleaned_text.strip()) < 10:
        # For very short texts, use a simpler approach
        english_indicators = ['the', 'and', 'ing', 'tion', 'ere', 'ent', 'tha']
        text_lower = cleaned_text.lower()
        score = sum(1 for indicator in english_indicators if indicator in text_lower)
        return score >= 1
        
    try:
        # Use langdetect for more accurate language detection
        language = detect(cleaned_text)
        return language == 'en'
    except:
        return False

def crack_caesar(cipher_text):
    cipher_text = cipher_text.upper()
    possible_solutions = []
    
    for key in range(len(ALPHABET)):
        plain_text = ''
        for c in cipher_text:
            if c == ' ':  # Preserve spaces
                plain_text += ' '
            elif c in ALPHABET:
                index = ALPHABET.find(c)
                index = (index - key) % len(ALPHABET)
                plain_text += ALPHABET[index]
            else:
                plain_text += c  # Preserve punctuation or unknown characters
        
        if detect_language(plain_text):
            possible_solutions.append((key, plain_text))
    
    if possible_solutions:
        print("[✔] Valid Decryption(s) Detected:")
        for key, text in possible_solutions:
            print(f"For key {key}: {text}")
            exit(0)
    else:
        print("[✗] No valid English decryption found.")

if __name__ == "__main__":
    data = input("Input the encrypted data: ")
    crack_caesar(data)