# @author Arjun Albert
# @email arjunalbert@brandeis.edu
# class to calculate minimum cost paths of adjacency lists
from HeapArray import MinHeapArray
import Constraints
from DisplayPath import DisplayPath
class MinimumCostPath:

    # load in vertices, edges, start, end and other args
    def __init__(self, vertices, edges, start, end, board, time):
        self.vertices = vertices
        self.edges = edges
        self.start = self.get_vertex_from_label(start)
        self.start_name = start
        self.end = self.get_vertex_from_label(end)
        self.end_name = end
        print(start, end)
        self.board = board.lower() == "y"
        self.time = time.lower() == "y"
        self.min_heap = MinHeapArray()
        self.distance_to_vertex_dict = {v : Constraints.InfiniteCost for v in vertices}
        self.time_to_vertex_dict = {v : Constraints.InfiniteCost for v in vertices}
        self.edgesTraversed = []
        for v in self.vertices:
            v.previous = None
            v.previousEdge = None

    
    # get a vertex from it's label
    def get_vertex_from_label(self, label):
        if label:
            for v in self.vertices:
                if v.label == label:
                    return v
            for v in self.vertices:
                if label in v.name.lower().strip():
                    return v


    # get starting node
    def get_start(self):
        return self.start


    # get end node
    def get_end(self):
        return self.end


    # get shortest path based on time/distance
    def shortest_path(self):
        if self.time:
            self.shortest_time_path()
        else:
            self.shortest_distance_path()


    # calculate shortest path by distance using Dijkstra
    def shortest_distance_path(self):
        self.distance_to_vertex_dict[self.get_start()] = 0
        for t in self.distance_to_vertex_dict.items():
            self.min_heap.insert(t)
        while not self.min_heap.isEmpty():
            t = self.min_heap.deleteMin()
            if t:
                cv = t[0]
                for e in self.get_adj_edges(cv):
                    new_dist = e.length + self.distance_to_vertex_dict.get(cv)
                    nv = self.get_vertex_from_label(e.label2)
                    if new_dist < self.distance_to_vertex_dict.get(nv):
                        self.distance_to_vertex_dict[nv] = new_dist
                        self.min_heap.decreaseValue(nv, new_dist)
                        nv.set_previous(cv)
                        nv.set_previous_edge(e)
                      
                        
    # calculate shortest path by time using Dijkstra
    def shortest_time_path(self):
        self.distance_to_vertex_dict[self.get_start()] = 0
        for t in self.distance_to_vertex_dict.items():
            self.min_heap.insert(t)
        while not self.min_heap.isEmpty():
            t = self.min_heap.deleteMin()
            if t:
                cv = t[0]
                for e in self.get_adj_edges(cv):
                    new_dist = self.getEdgeTime(e) + self.distance_to_vertex_dict.get(cv)
                    nv = self.get_vertex_from_label(e.label2)
                    if new_dist < self.distance_to_vertex_dict.get(nv):
                        self.distance_to_vertex_dict[nv] = new_dist
                        self.min_heap.decreaseValue(nv, new_dist)
                        nv.set_previous(cv)
                        nv.set_previous_edge(e)


    # display route found to console
    def displayRoute(self):
        dp = DisplayPath(self.edgesTraversed, self.vertices)
        dp.draw() 


    # print out the visited edges in order
    def printout_path(self, output_file):
        try:
            vList = self.get_previous_vertex_list(self.get_end(), [])
            vList.reverse()
            legs = 0; distance = 0; time = 0
            for v in vList:
                if v:
                    e = v.previousEdge
                    if e: 
                        self.edgesTraversed.append(e)
                        d, t = self.printEdge(e, output_file)
                        distance += d; time += t; legs += 1
            print(f'legs = {legs}, distance = {distance} feet, time = {round(time/60, 1)} minutes', file = output_file)
        except Exception as e:
            # print(e)
            print(f'Could not find path between {self.start_name} and {self.end_name}', file = output_file)


    # print single edge based on skating/ walking
    def printEdge(self, e, of):
        if self.board:
            return self.printSkatingEdge(e, of)
        return self.printWalkingEdge(e, of)


    # get time to traverse an edge based on skating/ walking
    def getEdgeTime(self, e):
        if self.board:
            return self.getSkatingTimeSeconds(e)
        return self.getWalkingTimeSeconds(e)


    # print an edge if walking
    def printWalkingEdge(self, e, output_file):
        v1 = self.get_vertex_from_label(e.label1)
        v2 = self.get_vertex_from_label(e.label2)
        print('FROM: (' + e.label1 + ') ' + str(v1), file = output_file)
        if e.name:
            print('ON: ' + e.name, file = output_file)
        print('Walk ' + str(e.length) + ' feet in direction ' + str(e.angle) + ' degrees ' + e.direction + '.', file = output_file)
        print('TO: (' + e.label2 + ') ' + str(v2), file = output_file)
        t = self.walkingTime(e)
        print('(' + str(t[0]) + ' ' + str(t[1]) + ')\n', file = output_file)
        print(file = output_file)
        if isinstance(t[0], float):
            return (e.length, round(t[0] * 60))
        return (e.length, t[0])


    # print an edge if skating
    def printSkatingEdge(self, e, output_file):
        v1 = self.get_vertex_from_label(e.label1)
        v2 = self.get_vertex_from_label(e.label2)
        print('FROM: (' + e.label1 + ') ' + str(v1), file = output_file)
        if e.name:
            print('ON: ' + e.name, file = output_file)
        board_not_allowed = e.surfaceType == 'bridge' or e.surfaceType == 'steps up' or e.surfaceType == 'steps down' or not e.boards_allowed
        moveType = 'Walk'
        if not board_not_allowed:
           moveType = 'Glide'
           if e.surfaceType == 'downhill':
               moveType = 'Coast down'
        elif e.surfaceType == 'steps down':
            moveType = 'Go down'
        elif e.surfaceType == 'steps up':
            moveType = 'Go up'
        print(moveType + ' ' + str(e.length) + ' feet in direction ' + str(e.angle) + ' degrees ' + e.direction + '.', file = output_file)
        print('TO: (' + e.label2 + ') ' + str(v2), file = output_file)
        t = self.skatingTime(e)
        if not board_not_allowed:
            print('(' + str(t[0]) + ' ' + str(t[1]) + ')', file = output_file)
        else:
            print('(no skateboards allowed, ' + str(t[0]) + ' ' + str(t[1]) + ')\n', file = output_file)
        print(file = output_file)
        if isinstance(t[0], float):
            return (e.length, round(t[0] * 60))
        return (e.length, t[0])


    # get time to traverse an edge walking
    def getWalkingTimeSeconds(self, e):
        if e.surfaceType == 'flat':
            return e.length / Constraints.WalkSpeed
        elif e.surfaceType == 'uphill':
            return e.length / (Constraints.WalkSpeed * Constraints.WalkFactorU)
        elif e.surfaceType == 'downhill':
             return e.length / (Constraints.WalkSpeed * Constraints.WalkFactorD)
        elif e.surfaceType == 'steps up':
            return e.length / (Constraints.WalkSpeed * Constraints.StepFactorU)
        elif e.surfaceType == 'steps down':
            return e.length / (Constraints.WalkSpeed * Constraints.StepFactorD)
        else:
            return e.length / (Constraints.WalkSpeed * Constraints.BridgeFactor)


    # convert walking time to mins/ secs
    def walkingTime(self, e):
        flatTime = self.getWalkingTimeSeconds(e)
        if flatTime >= 1:
            return (round(flatTime, 1), 'minutes')
        elif flatTime == 1:
            return (round(flatTime, 1), 'minute') 
        else:
            return (round(flatTime * 60), 'seconds')


    # get time to traverse an edge skating
    def getSkatingTimeSeconds(self, e):
        if e.boards_allowed:
            if e.surfaceType == 'flat':
                return e.length / (Constraints.WalkSpeed * Constraints.SkateFactorF)
            elif e.surfaceType == 'uphill':
                return e.length / (Constraints.WalkSpeed * Constraints.SkateFactorU)
            elif e.surfaceType == 'downhill':
                return e.length / (Constraints.WalkSpeed * Constraints.SkateFactorD)
            elif e.surfaceType == 'steps up':
                return e.length / (Constraints.WalkSpeed * Constraints.StepFactorU)
            elif e.surfaceType == 'steps down':
                return e.length / (Constraints.WalkSpeed * Constraints.StepFactorD)
            else:
                return e.length / (Constraints.WalkSpeed * Constraints.BridgeFactor)
        else:
            return self.getWalkingTimeSeconds(e)


    # convert skating time to mins/ secs
    def skatingTime(self, e):
        flatTime = self.getSkatingTimeSeconds(e)
        if flatTime > 1:
            return (round(flatTime, 1), 'minutes')
        elif flatTime == 1:
            return (round(flatTime, 1), 'minute') 
        else:
            return (round(flatTime * 60), 'seconds')


    # traverse from a node to get previous path
    def get_previous_vertex_list(self, vertex, vList):
        vList.append(vertex)
        if vertex.previous:
            return self.get_previous_vertex_list(vertex.previous, vList)
        return vList


    # get adjacent vertices to a vertex
    def get_adj_vertices(self, vertex):
        adjs = []
        for e in self.edges:
            if e.label1 == vertex.label:
                adjs.append(self.get_vertex_from_label(e.label2))
        return adjs


    # get adjacent edges to a vertex
    def get_adj_edges(self, vertex):
        adjs = []
        for e in self.edges:
            if e.label1 == vertex.label:
                adjs.append(e)
        return adjs 


    # get shortest distance to end of path
    def get_shortest_distance(self):
        return self.distance_to_vertex_dict.get(self.get_end())


    # print distance to vertex list for debugging
    def display(self):
        for x, y in self.distance_to_vertex_dict.items():
            print(x, y)