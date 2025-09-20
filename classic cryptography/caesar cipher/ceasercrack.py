ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # Removed space from the alphabet

def crack_caesar(cipher_text):
    cipher_text = cipher_text.upper()
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
        print(f"For key {key}: {plain_text}")

if __name__ == "__main__":
    data = input("Input the encrypted data: ")
    crack_caesar(data)


