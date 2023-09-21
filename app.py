from flask import Flask, render_template, request
import ast

website = Flask(__name__)
filename = 'eng_voc.txt'

with open(filename, 'r') as file:
    word_set = ast.literal_eval(file.read())

class SpellChecker:
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def levenshtein_distance(self, word1, word2):
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0:
                    dp[i][j] = j    #insert
                elif j == 0:
                    dp[i][j] = i    #delete
                elif word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]     #nothing
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])    #replace
        return dp[m][n]

    def spell_check(self, input_word):
        if input_word in self.dictionary:
            return None
        
        suggestions = []
        for word in self.dictionary:
            distance = self.levenshtein_distance(input_word, word)
            if distance <= 2: 
                suggestions.append((word, distance))

        if suggestions:
            closest_word, _ = min(suggestions, key=lambda x: x[1])
            return closest_word
        else:
            return "Incorrect. No suggestions found."
    
    def suggest_extra(self, input_word):
        extra = []

        for word in self.dictionary:
            if word.startswith(input_word):
                extra.append(word)
        return extra

@website.route('/', methods=['GET', 'POST'])
def index():
    output = None
    form_field = None

    if request.method == 'POST':
        input_word = request.form['user_input_spellchecker']
        form_field = {'input' : input_word}
        
        spell_checker = SpellChecker(word_set)
        
        misspelled = spell_checker.spell_check(input_word)
        extra = spell_checker.suggest_extra(input_word)
        
        if misspelled:
            if (misspelled == "Incorrect. No suggestions found."):
                output = {'message' : misspelled}
            else:
                output = {'message' : 'Incorrect. Check for suggestions below.', 'sugg_distance' : str(misspelled), 'sugg_extra' : str(extra)}
        else:
            output = {'message' : 'No Misspelled Words', 'sugg_extra' : str(extra)}
    
    return render_template('index.html', output = output, form_field = form_field)

if __name__ == '__main__':
    website.run(debug=True)