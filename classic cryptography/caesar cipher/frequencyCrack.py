import matplotlib.pylab as plt
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def frequency_analysis(text):
    text = text.upper()
    letter_freq = {}
    #Frequency init
    for letter in LETTERS:
        letter_freq[letter] = 0
    #counting letters
    for letter in text:
        if letter in LETTERS:
            letter_freq[letter] += 1
    #return letters and their frequencies
    return letter_freq


def plot_distribution(frequencies):
    plt.bar(frequencies.keys(), frequencies.values())
    plt.show()

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
            plain_text += c  # preserve punctuation or unknown characters
    return plain_text

def caesar_crack(ciphertext):
    freq = frequency_analysis(ciphertext)
    plot_distribution(freq)
    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    print(freq)
    keys = {}
    for i in range(5):
        keys[i] = (LETTERS.find(freq[i][0]) - LETTERS.find('E'))
    print("The possible key value: %s" % keys)
    for key in keys:
        print("The decrypted message: [ ", ceaser_decrypt(keys[key], ciphertext), " ]")

if __name__ == "__main__":
    ciphertext = "LQSXW D PHVVDJH:IRU DOO ZH KDYH WR GR LV WR PRYH IRUZDUG. QRW IRU JORUB, QRW IRU UHFRJQLWLRQ, EXW IRU WKH VDNH RI WKRVH ZKR FDPH EHIRUH XV, IRU WKH IXWXUH ZH VWULYH WR FUHDWH, IRU WKH OHJDFB ZH LQWHQG WR OHDYH EHKLQG. ZH ZLOO PRYH IRUZDUG, WRJHWKHU, XQWLO RXU ILQDO EUHDWK"
    caesar_crack(ciphertext) 