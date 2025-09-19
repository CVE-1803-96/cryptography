ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KEY = 3

def ceaser_encrypt(plaintext, KEY):
    cipher_text = ''
    plaintext = plaintext.upper()

    for c in plaintext:
        if c == ' ':
            cipher_text += ' '  # preserve the space
        elif c in ALPHABET:
            index = ALPHABET.find(c)
            index = (index + KEY) % len(ALPHABET)
            cipher_text += ALPHABET[index]
        else:
            cipher_text += c  

    return cipher_text



def ceaser_decrypt(KEY, ciphertext):
    plain_text = ''
    for c in ciphertext:
        if c == ' ':
            plain_text += ' '
        elif c in LETTERS:
            index = LETTERS.find(c)
            index = (index - KEY) % len(LETTERS)
            plain_text += LETTERS[index]
        else:
            plain_text += c  
    return plain_text


if __name__ == "__main__":
    data = input("Input a message:")
    mode = input("The mode: (E/D)")
    if mode == 'E':
        print(ceaser_encrypt(data, KEY))
    elif mode == 'D':
        print(ceaser_decrypt(data, KEY))
    else:
        print("Wrong mode. !")



    