"""
This file implements a solver for the crossword problem.
It models the problem using segments and letters.

This model works fine on big crosswords because the number of letters is 27.
However, it can output a result that uses the same word twice. This makes it much faster
but prevent it from proving that there is no solution in some cases.
"""

from constraint_programming import constraint_programming
from crossword_parsing import Crossword, read_words
import string
import datetime

WORDS = "../../words2.txt"
CROSSWORD = "../../crossword2.txt"

def letters_positions_from(solution):
    positions = []
    for key, value in solution.items():
        if type(value)==str:
            if len(value)==1:
                letter = value
                position = key
                positions.append((letter, position))
    return positions
                
def solve(words, crossword):
    # The variables are the letters in each case and the words in each segment
    cases = []
    # Get all the cases that are in a segment
    for segment in cw.hsegments+cw.vsegments:
        cases += segment.get_points()
    cases = set(cases)
    # Each case can contain one letter from the alphabet
    var = {case: set([letter for letter in list(string.ascii_lowercase)]) for case in cases}
    # Each segment can contain a word from the list of words allowed
    for segment in cw.hsegments+cw.vsegments:
        var[str(segment)] = set([word for word in words[segment.length()]])

    P = constraint_programming(var)

    # A segment's word is composed of the letters contained in the cases that compose the segment
    for segment in cw.hsegments+cw.vsegments:
        for case in segment.get_points():
            if segment.is_horizontal():
                i = case[0] - segment.origin[0]
            elif segment.is_vertical():
                i = case[1] - segment.origin[1]
            CASE_FROM_SEGMENT = {(word, word[i]) for word in words[segment.length()]}
            P.addConstraint(str(segment), case, CASE_FROM_SEGMENT)
    sol = P.solve()
    letters_positions = letters_positions_from(sol)
    return letters_positions

if __name__=="__main__":
    start = datetime.datetime.now()
    # Get words
    words = read_words(WORDS)
    # Get crossword
    cw = Crossword(CROSSWORD)
    # Solve the problem for words and cw
    letters_positions = solve(words, cw)
    end = datetime.datetime.now()
    duration = end-start
    cw.display_solution(letters_positions)
    print("The result was computed in {}".format(duration))