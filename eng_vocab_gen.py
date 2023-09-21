from nltk import download
from nltk.corpus import words

download("words")

english = set(w.lower() for w in words.words())

# print(english)

filename = 'eng_voc.txt'

with open(filename, 'w') as f:
    f.write(str(english))  