# @author Arjun Albert
# @email arjunalbert@brandeis.edu
# import custom classes
from MapEdge import MapEdge
from MapVertex import MapVertex
from MinimumCostPath import MinimumCostPath
from TourGuide import TourGuide
# import system class to get proper end of 
# line characters as well as file object for printing
import sys

# adjacency list of vertices and edges
all_vertices = []
all_edges = []

# default repl values
DEFAULT_VERTICES = 'MapDataVertices.txt'
DEFAULT_EDGES = 'MapDataEdges.txt'
SKATEBOARD_PROMPT = 'Have a skateboard (y/n - default=n)? '
TIME_PROMPT = 'Minimize time (y/n - default=n)? '
START_PROMPT = 'Enter start (return to quit): '
FINISH_PROMPT = 'Enter finish (or return to do a tour): '
INVALID = 'Invalid input, please try again.'
TOURS = ['simple-hamilton', 'simple-prims', 'shortcut-prims', 'kruskals']
TOUR_PROMPT = f'What type of tour:\n[Simple Hamilton Tour - {TOURS[0]}]\n[Prims MST - {TOURS[1]}]\n[Prims with Shorcutting - {TOURS[2]}]\n[Kruskals Tour - {TOURS[3]}]\n'

# default printing, output to file, and display map values
DISPLAY_MAP = True
# sample = open('sample.txt', 'w') 
# OUTPUT_FILE = sample
OUTPUT_FILE = sys.stderr


# load all the vertices as objects from a text file
def load_vertices(txtFile):
    with open(txtFile, 'r') as vertices:
        for line in vertices:
            v = load_vertex(line)
            if v:
                all_vertices.append(v)
    return all_vertices


# load all the edges as objects from a text file
def load_edges(txtFile):
    with open(txtFile, 'r') as edges:
        for line in edges:
            l = load_edge(line)
            if l:
                all_edges.append(l)
    return all_edges


# create a vertex object from a line of text
def load_vertex(line):

    # remove black hole vertex
    if "//" not in line and len(line) > 1:
        name = extract_name(line)
        if name != 'Black Hole':
            line = line.split(' ')
            args = [l for l in line][0:4]
            return MapVertex(*args, name)


# create an edge object from a line of text
def load_edge(line):
    if "//" not in line and len(line) > 1:
        st = extract_surface(line)
        name = extract_name(line)
        line = line.split(' ')
        args = [l for l in line][0:8]
        return MapEdge(*args, st, name)
    

# grab a "name" from a line of text 
def extract_name(line):
    fi = line.index('"', 0)
    return line[fi + 1: len(line) - 2]


# grab the (surface type) from a line of text
def extract_surface(line):
    fi = line.index('(', 0)
    return line[fi + 1: fi + 2]


# prompt user and get starting input
def start_prompt():
    print('\n************* WELCOME TO THE BRANDEIS MAP *************')
    return input(START_PROMPT)


# load edges/ vertices
load_vertices(DEFAULT_VERTICES)
load_edges(DEFAULT_EDGES)

# prompt user and start repl
start = start_prompt()
while start:

    # try except statement to catch bad input
    # try:
        
        # get default argument values
    end = input(FINISH_PROMPT)
    tour = not end
    board, time = ('n', 'n')
    if tour: 

        # get tour type
        tour_type = input(TOUR_PROMPT)

        # get board and time arguments for tours
        if tour_type is not TOURS[0]:
            board = input(SKATEBOARD_PROMPT)
            time = input(TIME_PROMPT)

        # create object to calculate different tours
        tg = TourGuide(all_vertices, all_edges, start, tour_type, board, time)

        # print and calculate tour
        tg.calculate_tour()

        # show results
        tg.printout_path(OUTPUT_FILE)
        if DISPLAY_MAP: tg.displayRoute()            
    else:

        # get board and time arguments
        board = input(SKATEBOARD_PROMPT)
        time = input(TIME_PROMPT)

        # create minimum cost path object 
        mcp = MinimumCostPath(all_vertices, all_edges, start, end, board, time)

        # calculate shortest path
        mcp.shortest_path()

        # show results
        mcp.printout_path(OUTPUT_FILE)
        if DISPLAY_MAP: mcp.displayRoute()
    # except Exception as e:
    #     print(e)
    #     # reprompt for valid input in case of exception
    #     print(INVALID)    
    start = start_prompt()