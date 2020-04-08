# @author Arjun Albert
# @email arjunalbert@brandeis.edu
# class to store an edge
class MapEdge:
    def __init__(self, number, label1, label2, v1, v2, length, angle, direction, st, name):
        self.number = int(number)
        self.label1 = label1
        self.label2 = label2
        self.v1 = int(v1)
        self.v2 = int(v2)
        self.length = int(length)
        self.angle = int(angle)
        self.direction = direction
        self.surfaceType = self.get_surface_type(st)
        self.name = name
        self.boards_allowed = self.boards_okay(st)
        self.st = st


    # get type of surface as full string
    def get_surface_type(self, st):
        return {'f': 'flat',
                'u': 'uphill',
                'd': 'downhill',
                'x': 'flat',
                's': 'steps up',
                't': 'steps down',
                'b': 'bridge'}.get(st.lower(), None)


    # return if boards are allowed on this edge
    def boards_okay(self, st):
        return not st.islower() or st == 'x'

    
    # create to string for edge
    def __str__(self):
        return "" + self.name + ", 1. " + self.label1 + ", 2. " + self.label2