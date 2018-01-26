from constraint_programming import constraint_programming
from crossword_parsing import Crossword, read_words

WORDS = "../words2.txt"
CROSSWORD = "../crossword2.txt"

words = read_words(WORDS)
cw = Crossword(CROSSWORD)

print("Creating var")
var = {str(line): set([word for word in words[line.length()]]) for line in cw.hlines+cw.vlines}
P = constraint_programming(var)

def get_intersection_possibilities(i, j, hlength, vlength):
    return {(word, other_word) for word in words[hlength] for other_word in words[vlength] if (word[i]==other_word[j] and word!=other_word)}

i = 0
for intersection in cw.intersections:
    i += 1
    print("Creating intersection {}".format(i))
    which_h = intersection['which'][0]
    hline = cw.hlines[which_h]
    which_v = intersection['which'][1]
    vline = cw.vlines[which_v]
    SAME_LETTER_INTERSECT = get_intersection_possibilities(*intersection['position_in_lines'], hline.length(), vline.length())
    P.addConstraint(str(hline), str(vline), SAME_LETTER_INTERSECT)


lines = cw.hlines + cw.vlines

print("Creating NEQ")
# A word is used only once
def get_neq(length): # classer les mots par taille
        NEQ = {(word, other_word) for word in words[length] for other_word in words[length] if (word!=other_word)}
        return NEQ

for line in lines:
    for other_line in lines:
        if line!=other_line:
            if line.length()==other_line.length():
                NEQ = get_neq(line.length())
                if NEQ:
                    P.addConstraint(str(line), str(other_line), NEQ)

print("Solving")
sol = P.solve()
print(sol)
