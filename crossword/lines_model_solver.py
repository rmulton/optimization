"""
This file implements a solver for the crossword problem.
It models the problem using segments.
    - Each segment must be attributed with a word that has the size of the segment
    - Two segments cannot be attributed with the same words
    - Two segments that intersect must have the same letter at the intersection

This model works fine on small crosswords. However, it can freeze the computer or take
to terminate if the crossoword is big. The reasons are :
    - The NEQ and SAME_LETTER_INTERSECT constraints requires n^2 instructions in the worst case, 
    with n the number of words.
    - The program has to hold the words in memory a lot of time, which can fill the memory
"""
from constraint_programming import constraint_programming
from crossword_parsing import Crossword, read_words
import datetime

WORDS = "../../words3.txt"
CROSSWORD = "../../crossword1.txt"

def solve(words, crossword):
    # A segment can only contain a word that has its size
    var = {str(segment): set([word for word in words[segment.length()]]) for segment in cw.hsegments+cw.vsegments}
    P = constraint_programming(var)

    # For convenience
    segments = cw.hsegments + cw.vsegments

    # A word can only be used once
    for length in words.keys():
        print("Creating NEQ for length {}".format(length))
        NEQ = {(word, other_word) for word in words[length] for other_word in words[length] if (word!=other_word)}
        segments_of_length = [segment for segment in segments if segment.length()==length]
        for segment in segments_of_length:
            for other_segment in segments_of_length:
                if segment!=other_segment:
                    P.addConstraint(str(segment), str(other_segment), NEQ)

    # Two segments that intersect must have the same letter at the intersection
    for intersection in cw.intersections:
        # Horizontal segment information
        which_h = intersection['which'][0]
        hsegment = cw.hsegments[which_h]
        hposition = intersection["position_in_segments"][0]
        hlength = hsegment.length()
        # Vertical segment information
        which_v = intersection['which'][1]
        vsegment = cw.vsegments[which_v]
        vposition = intersection["position_in_segments"][1]
        vlength = vsegment.length()
        # Constraint
        SAME_LETTER_INTERSECT = {(word, other_word) for word in words[hlength] for other_word in words[vlength] if (word[hposition]==other_word[vposition] and word!=other_word)}
        P.addConstraint(str(hsegment), str(vsegment), SAME_LETTER_INTERSECT)

    sol = P.solve()
    return sol

if __name__=="__main__":
    start = datetime.datetime.now()
    # Get words
    words = read_words(WORDS)
    # Get crossword
    cw = Crossword(CROSSWORD)
    # Solve the problem for words and cw
    sol = solve(words, cw)
    end = datetime.datetime.now()
    duration = end-start
    print(sol)
    print("The result was computed in {}".format(duration))
