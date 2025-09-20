
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

#The main function:

get_data()
plain_text = "In this guide, you'll learn how to tackle almost every challenge in cryptohack. Familiarize yourself with downloading a starter Python script to solve given problems—this is a common method used in crypto CTF challenges"
print(is_text_english(plain_text))