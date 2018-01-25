import re
import math

WORDS = "../words2.txt"
CROSSWORD = "../crossword2.txt"

def read_words(path):
    f = open(path, "r")
    lines = f.readlines()
    words = dict()
    for line in lines:
        word = line.strip()
        length = len(word)
        if length in words.keys():
            words[length] += [word]
        else:
            words[length] = [word]
    return words

words = read_words(WORDS)

hashes_regex = re.compile("\.+")

class Line:
    def __init__(self, origin, end):
        self.origin = origin
        self.end = end
    def __repr__(self):
        return "<origin: {}, end: {}>".format(str(self.origin), str(self.end))
    def length(self):
        return max(math.fabs(self.origin[0] - self.end[0]), math.fabs(self.origin[1] - self.end[1]))+1
    def get_type(self):
        if self.is_vertical():
            return "vertical"
        if self.is_horizontal():
            return "horizontal"
    def is_vertical(self):
        return self.origin[0]==self.end[0] and self.origin[1]!=self.origin[1]
    def is_horizontal(self):
        return self.origin[1]==self.end[1] and self.origin[0]!=self.origin[0]
    

def parse_horizontally(path):
    f = open(path, "r")
    horizontal_dots = []
    lines = f.readlines()
    for i, line in enumerate(lines):
        line = line.strip()
        positions = hashes_regex.finditer(line)
        for pos in positions:
            dot_line = Line((pos.span()[0], i), (pos.span()[1]-1, i))
            if dot_line.length()>1:
                horizontal_dots.append(dot_line)
    return horizontal_dots

def get_columns(path):
    f = open(path, "r")
    lines = f.readlines()
    columns = ['' for i in range(len(lines))]
    for line in lines:
        for caract in enumerate(line):
            if caract[1] != "\n":
                columns[caract[0]] += caract[1]
    return columns
    
# NB : the y axis is reversed
def parse_vertically(path):
    vertical_dots = []
    columns = get_columns(path)
    for i, column in enumerate(columns):
        positions = hashes_regex.finditer(column)
        for pos in positions:
            dot_column = Line((i, pos.span()[0]), (i, pos.span()[1]-1))
            if dot_column.length()>1:
                vertical_dots.append(dot_column)
    return vertical_dots

def read_crossword(path):
    # Horizontal lines
    horizontal_lines = parse_horizontally(path)
    # Vertical lines
    vertical_lines = parse_vertically(path)
    return horizontal_lines, vertical_lines
    
hlines, vlines = read_crossword(CROSSWORD)

def find_intersection(h_line, v_line):
    # Better: use the fact that it is necessary for the intersection to have v_line x position and h_line y position
    a = h_line.origin[0]<= v_line.origin[0]
    b = v_line.origin[0]<=h_line.end[0]
    c = v_line.origin[1]<=h_line.origin[1]
    d = v_line.origin[1]<= h_line.origin[1]
    e = h_line.origin[1]<=v_line.end[1]
    f = v_line.origin[0]>=h_line.origin[0]
    if a and b and c and d and e and f:
        return (v_line.origin[0], h_line.origin[1])
    else:
        return None

def find_intersections(hlines, vlines):
    intersections = []
    """
    [
        {
            "which": (
                nieme ligne de dots hlines,
                mieme colonne de dots vlines
                ),
            "position": (x, y)
    ]
    """
    for i, h_line in enumerate(hlines):
        for j, v_line in enumerate(vlines):
            intersection = find_intersection(h_line, v_line)
            if intersection != None:
                u = intersection[0] - h_line.origin[0]
                v = intersection[1] - v_line.origin[1]
                intersections.append({"position_in_crossword":intersection, "position_in_lines":(u, v), "which":(i, j)})
    return intersections

intersections = find_intersections(hlines, vlines)

class Crossword:
    def __init__(self, path):
        self.path = path
        self.find_lines()
        self.find_intersections()
    def find_lines(self):
        self.hlines, self.vlines = read_crossword(self.path)
    def find_intersections(self):
        self.intersections = find_intersections(self.hlines, self.vlines)
    def __repr__(self):
        return "horizontal lines: {}\nvertical lines: {}\nintersections: {}>".format(self.hlines, self.vlines, self.intersections)
        
cw = Crossword(CROSSWORD)

from constraint_programming import constraint_programming

print("Creating var")
var = {str(line): set([word for word in words[line.length()]]) for line in cw.hlines+cw.vlines}
P = constraint_programming(var)

def get_intersection_possibilities(i, j, hlength, vlength):
    return {(word, other_word) for word in words[hlength] for other_word in words[vlength] if (word[i]==other_word[j] and word!=other_word)}

i = 0
for intersection in intersections:
    i += 1
    print("Creating intersecton {}".format(i))
    which_h = intersection['which'][0]
    hline = hlines[which_h]
    which_v = intersection['which'][1]
    vline = vlines[which_v]
    SAME_LETTER_INTERSECT = get_intersection_possibilities(*intersection['position_in_lines'], hline.length(), vline.length())
    P.addConstraint(str(hline), str(vline), SAME_LETTER_INTERSECT)


lines = cw.hlines + cw.vlines

print("Creating NEQ")
# A word is used only once
def get_neq(length): # classer les mots par taille
        NEQ = {(word, other_word) for word in words[length] for other_word in words[length] if (word!=other_word)}
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
