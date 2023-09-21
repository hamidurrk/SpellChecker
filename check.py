import re, ast

filename = 'eng_voc.txt'

words_to_match = 'apple'
 
with open(filename, 'r') as f:
    english_vocab = ast.literal_eval(f.read())

def genSubSet(word_set):
    sub_set = set()
    for word in word_set:
        sub_set.add(word)
        for i in range(len(word)):
            for j in range(len(word) - i + 1):
                if word[j:j+i] != '':
                    sub_set.add(word[j:j+i])
    return sub_set

subSetList = genSubSet(words_to_match)
print(subSetList)
print(len(subSetList))

with open(filename, 'r') as f:

    file_contents = f.read().split()

    num_matches = 0
    num_partial_matches = []
    matchList = []
    totalList = []
    for word in words_to_match:
        matchList.append(0)
        totalList.append(0)

    for i in range(len(subSetList)):
        searchSet = subSetList[i]
        print('Searching %s' %searchSet)
        for word in file_contents:
            totalList[len(searchSet) - 1] += 1
            if searchSet == {word}:
                num_matches += 1
                matchList[len(searchSet) - 1] = num_matches

print('Number of matches: ')
print(matchList)
print(totalList)

accuracy = []
for i in range(len(matchList)):
    accuracy.append((matchList[i] / totalList[i]) * 100)
    print('%d word match found in %d places with occurrence probability of %.2f%%' % (i + 1, matchList[i], accuracy[i]))

print(accuracy)
