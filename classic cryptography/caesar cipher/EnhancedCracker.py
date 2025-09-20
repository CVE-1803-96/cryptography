ALPHABET = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ENGLISH_WORDS = []

def get_data():
    dictionary = open('words.txt', 'r')
    for word in dictionary.read().split("\n"):
        ENGLISH_WORDS.append(word.upper())
    dictionary.close()

def count_words(text):
    matches = 0
    text  = text.upper()
    words = text.split(' ')
    for word in words:
        if word in ENGLISH_WORDS:
            matches += 1
    return matches

def is_text_english(text):
    matches = count_words(text)
    if (float(matches) / len(text.split(' '))) * 100 >= 80:
        return True
    return False


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
        if(is_text_english(plain_text)):
            print("[✔] Valid Decryption Detected.")
            print(f"For key {key}: {plain_text}")
            exit(0)
                

if __name__ == "__main__":
    get_data()
    data = input("Input the encrypted data: ")
    crack_caesar(data)