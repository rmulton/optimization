from constraint_programming import constraint_programming
from crossword_parsing import Crossword, read_words
import string

"""
Does not check that words are differents from each other
"""

WORDS = "../words2.txt"
CROSSWORD = "../crossword2.txt"

words = read_words(WORDS)
cw = Crossword(CROSSWORD)

# Variable : letters on intersections
print("Creating var")
cases = []
for line in cw.hlines+cw.vlines:
    cases += line.get_points()
cases = set(cases)
var = {str(case): set([letter for letter in list(string.ascii_lowercase)]) for case in cases}
for line in cw.hlines+cw.vlines:
    var[str(line)] = set([word for word in words[line.length()]])

P = constraint_programming(var)

for line in cw.hlines+cw.vlines:
    for case in line.get_points():
        if line.is_horizontal():
            i = case[0] - line.origin[0]
        elif line.is_vertical():
            i = case[1] - line.origin[1]
        CASE_FROM_LINE = {(word, word[i]) for word in words[line.length()]}
        P.addConstraint(str(line), str(case), CASE_FROM_LINE)

sol = P.solve()
print(sol)