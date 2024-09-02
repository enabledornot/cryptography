import re
from collections import OrderedDict
def loadLetters():
    with open("letter_freq.txt","r",errors='ignore') as f:
        data = f.read().split("\n")
    letter_frequency = OrderedDict()
    for line in data:
        pattern = r"([a-z])\s+(\d+(\.\d+)?)%"
        match = re.search(pattern, line)
        if match:
            letter = match.group(1)
            frequency = match.group(2)
            letter_frequency[letter] = frequency
        else:
            print("ERROR:")
            print(line)
    return letter_frequency

def loadWords():
    with open("en_full.txt","r",errors='ignore') as f:
        data = f.read().split("\n")
    word_frequency = OrderedDict()
    for line in data:
        pattern = r"(\w+)\s(\d+)"
        match = re.search(pattern, line)
        if match:
            word = match.group(1)
            frequency = int(match.group(2))
            if frequency < 100:
                break
            if word not in word_frequency:
                word_frequency[word] = int(frequency)
        # else:
        #     print("ERROR:")
        #     print(line)
    return word_frequency

def readCodefile(fname):
    with open(fname,"r") as f:
        fdata = f.read().split("\n")
    words = []
    for line in fdata:
        words.append([])
        letters = line.split("	")
        for letter in letters:
            if letter == "":
                words.append([])
            else:
                try:
                    int(letter)
                except ValueError:
                    words.append([])
                else:
                    if len(letter) == 1:
                        letter = "0" + letter
                    words[-1].append(letter)
    return words
def words_by_length(words):
    words_by_length = [OrderedDict()]
    for i in range(max(len(key) for key in words)):
        words_by_length.append(OrderedDict())
    for word in words:
        words_by_length[len(word)][word] = words[word]
    return words_by_length