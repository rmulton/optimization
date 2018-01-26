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

WORDS = "../../words2.txt"
CROSSWORD = "../../crossword2.txt"

if __name__=="__main__":
    words = read_words(WORDS)
    cw = Crossword(CROSSWORD)

    # The variables are the letters in each case and the words in each segment
    cases = []
    # Get all the cases that are in a segment
    for segment in cw.hsegments+cw.vsegments:
        cases += segment.get_points()
    cases = set(cases)
    # Each case can contain one letter from the alphabet
    var = {str(case): set([letter for letter in list(string.ascii_lowercase)]) for case in cases}
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
            P.addConstraint(str(segment), str(case), CASE_FROM_SEGMENT)

    sol = P.solve()
    print(sol)