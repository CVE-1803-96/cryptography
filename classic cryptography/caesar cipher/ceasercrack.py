ALPHABET = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def crack_caesar(cipher_text):
    cipher_text = cipher_text.upper()
    for key in range(len(ALPHABET)):
        plain_text = ''
        for c in cipher_text:
            index = ALPHABET.find(c)
            index = (index - key) % len(ALPHABET)
            plain_text = plain_text + ALPHABET[index]
        print(f"For{key}: {plain_text}")


if __name__ == "__main__":
    data = input("Input the encrypted data: ")
    crack_caesar(data)
