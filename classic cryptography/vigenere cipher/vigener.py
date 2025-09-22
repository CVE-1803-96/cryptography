ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def vigenere_encrypt(plaintext, key):
    ciphertext = ''
    plaintext = plaintext.upper()
    key = key.upper()
    key_index = 0

    for char in plaintext:
        if char == ' ':  
            ciphertext += ' '
        elif char in ALPHABET:
            index = (ALPHABET.find(char) + ALPHABET.find(key[key_index])) % len(ALPHABET)
            ciphertext += ALPHABET[index]
            key_index += 1
            if key_index == len(key):
                key_index = 0
        else:
            ciphertext += char  
    return ciphertext

def vigenere_decrypt(ciphertext, key):
    plaintext = ''
    ciphertext = ciphertext.upper()
    key = key.upper()
    key_index = 0

    for char in ciphertext:
        if char == ' ':  
            plaintext += ' '
        elif char in ALPHABET:
            index = (ALPHABET.find(char) - ALPHABET.find(key[key_index])) % len(ALPHABET)
            plaintext += ALPHABET[index]
            key_index += 1
            if key_index == len(key):
                key_index = 0
        else:
            plaintext += char  
    return plaintext

if __name__ == "__main__":
    text = input("Input the text: ")
    secret = input("Input the secret key: ")
    ciphertext = vigenere_encrypt(text, secret)
    print("The ciphertext: ", ciphertext)
    plaintext = vigenere_decrypt(ciphertext, secret)
    print("The plaintext: ", plaintext)
