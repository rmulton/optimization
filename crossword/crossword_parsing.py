import re
import math

CASES_REGEX = re.compile("\.+")

############################
### Read words<name>.txt ###
############################

def read_words(path):
    """
    Takes a path to the txt document that contains the list of authorized words.
    Returns a dictionnary that contains the words sorted by length
    {1: [word of size 1, other word of size 1, ...], ...}
    """
    file = open(path, "r")
    lines = file.readlines()
    words = dict()
    for line in lines:
        word = line.strip()
        word = word.lower()
        length = len(word)
        if length in words.keys():
            words[length] += [word]
        else:
            words[length] = [word]
    return words

################################
### Read crossword<name>.txt ###
################################

# Warnings:
#   - only implemented for square crosswords
#   - y axis is reversed

class Segment:
    """
    A segment is a string of empty cases that we want to fill with a word.
    """
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
        return self.origin[0]==self.end[0] and self.origin[1]!=self.end[1]
    def is_horizontal(self):
        return self.origin[1]==self.end[1] and self.origin[0]!=self.end[0]
    def get_points(self):
        if self.is_horizontal():
            return [(i, self.origin[1]) for i in range(self.origin[0], self.end[0]+1)]
        elif self.is_vertical():
            return [(self.origin[0], i) for i in range(self.origin[1], self.end[1]+1)]
        else:
            print("Error")

def parse_horizontally(path):
    f = open(path, "r")
    horizontal_dots = []
    lines = f.readlines()
    for i, line in enumerate(lines):
        line = line.strip()
        positions = CASES_REGEX.finditer(line)
        for pos in positions:
            dot_segment = Segment((pos.span()[0], i), (pos.span()[1]-1, i))
            if dot_segment.length()>1:
                horizontal_dots.append(dot_segment)
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
        positions = CASES_REGEX.finditer(column)
        for pos in positions:
            dot_column = Segment((i, pos.span()[0]), (i, pos.span()[1]-1))
            if dot_column.length()>1:
                vertical_dots.append(dot_column)
    return vertical_dots

def read_crossword(path):
    # Horizontal segments
    horizontal_segments = parse_horizontally(path)
    # Vertical segments
    vertical_segments = parse_vertically(path)
    return horizontal_segments, vertical_segments
    
def find_intersection(h_segment, v_segment):
    # Better: use the fact that it is necessary for the intersection to have v_segment x position and h_segment y position
    a = h_segment.origin[0]<= v_segment.origin[0]
    b = v_segment.origin[0]<=h_segment.end[0]
    c = v_segment.origin[1]<=h_segment.origin[1]
    d = v_segment.origin[1]<= h_segment.origin[1]
    e = h_segment.origin[1]<=v_segment.end[1]
    f = v_segment.origin[0]>=h_segment.origin[0]
    if a and b and c and d and e and f:
        return (v_segment.origin[0], h_segment.origin[1])
    else:
        return None

def find_intersections(hsegments, vsegments):
    intersections = []
    """
    Trouve les intersections entre les segments hsegments et vsegments.
    Elles sont retournées dans une liste de dictionnaires décrit ci-dessous:
    [
        {
            "which": (n, m),
            "position_in_crossword": (x, y),
            "position_in_segments": (u, v)
        },
        ...
    ]
    Avec :
        - n (respectivement m) est l'indice du segment horizontal (respectivement vertical)
        concerné par l'intersection
        - position_in_crossword représente la position de l'intersection dans le damier
        - position_in_segments représente la position de l'intersection dans les segments
        (u est la position dans le segment horizontal, v dans le segment vertical)
    """
    for i, h_segment in enumerate(hsegments):
        for j, v_segment in enumerate(vsegments):
            intersection = find_intersection(h_segment, v_segment)
            if intersection != None:
                u = intersection[0] - h_segment.origin[0]
                v = intersection[1] - v_segment.origin[1]
                intersections.append({"position_in_crossword":intersection, "position_in_segments":(u, v), "which":(i, j)})
    return intersections

def read_crossword_size(path):
    """
    Trouve la taille d'un damier carré à partir de son fichier txt
    """
    f = open(path, "r")
    segment = f.readline()
    segment = segment.strip()
    return len(segment)

class Crossword:
    """
    A Crossword is the result of the parser on a txt file that represent a crossword.
    It contains:
        - the segments
        - the intersections between the segments
        - the size of the crossword
    WARNING : this class is only implemented for square crosswords
    """
    def __init__(self, path):
        self.path = path
        self.find_segments()
        self.find_intersections()
        self.find_size()
    def find_segments(self):
        self.hsegments, self.vsegments = read_crossword(self.path)
    def find_intersections(self):
        self.intersections = find_intersections(self.hsegments, self.vsegments)
    def find_size(self):
        self.size = read_crossword_size(self.path)
    def __repr__(self):
        return "horizontal segments: {}\nvertical segments: {}\nintersections: {}>".format(self.hsegments, self.vsegments, self.intersections)
    def display_solution(self, letters_positions):
        display_crossword_with_letters(self.path, letters_positions)
        
def display_crossword_with_letters(path, letters_positions):
    f = open(path)
    lines = f.read().split("\n")
    for letter, position in letters_positions:
        line = lines[position[1]]
        line = line[:position[0]] + letter + line[position[0]+1:]
        lines[position[1]] = line
    for line in lines:
        line = extend_line(line)
        print(line)

def extend_line(line):
    new_line = ""
    for letter in line:
        new_line += letter+ " "
    return new_line