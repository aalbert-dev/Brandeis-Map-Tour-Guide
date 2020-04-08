# @author Arjun Albert
# @email arjunalbert@brandeis.edu
# class to store a vertex
class MapVertex:
    def __init__(self, number, label, x, y, name):
        self.number = int(number)
        self.label = str(label)
        self.x = int(x)
        self.y = int(y)
        self.name = name
        self.previous = None
        self.previousEdge = None
        self.skipped = False

    # to string for printing
    def __str__(self):
        return self.name


    # get previous vertex
    def set_previous(self, vertex):
        self.previous = vertex


    # get previous edge
    def set_previous_edge(self, edge):
        self.previousEdge = edge

    