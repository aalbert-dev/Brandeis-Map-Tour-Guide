# @author Arjun Albert
# @email arjunalbert@brandeis.edu
# class to calculate tour of map
from HeapArray import MinHeapArray
from NTree import NTree
import Constraints
class TourGuide:
    def __init__(self, vertices, edges, start, tourType, board, time):
        self.vertices = vertices
        self.edges = edges
        self.start = start
        self.tourType = tourType
        self.board = board.lower() == "y"
        self.time = time.lower() == "y"
        self.visited = []
        self.edgesTraversed = []
        self.MSTValues = {v : Constraints.InfiniteCost for v in vertices}
        self.KMSTValues = {e : self.getEdgeCost(e) for e in edges}
        self.Kforest = []
        self.shortcutVisited = []
        self.mst = None


    # display route found to console
    def displayRoute(self):
        from DisplayPath import DisplayPath
        dp = DisplayPath(self.edgesTraversed, self.vertices)
        dp.draw() 


    # calculate tour of some type -
    def calculate_tour(self):
        return {'simple-hamilton' : self.calculateHamiltonPath,
                'simple-prims' : self.calculatePrims,
                'shortcut-prims' : self.calculatePrimsWithShortcut,
                'kruskals' : self.calculateKruskals}.get(self.tourType)()


    # calculate a MST with kruskals algorithm and get the preorder traversal for a tour
    # use a forest of trees as set data structure with union and find operations
    def calculateKruskals(self):

        # create min heap to hold edges in increasing order
        mh = MinHeapArray() 
        for t in self.KMSTValues.items():
            mh.insert(t)

        # insert each vertex as it's own tree in the forest
        for v in self.vertices:
            nt = NTree()
            nt.addRootVertex(v)
            self.Kforest.append(nt)

        # Pick the first V - 1 edges in increasing order of cost
        edges_added = 0
        while edges_added < len(self.vertices) and not mh.isEmpty():
            t = mh.deleteMin()
            if t:

                # if the two vertices in the picked edge are not in the same set
                ce = t[0]; l1 = ce.label1; l2 = ce.label2
                if not self.checkSameTree(l1, l2):

                    # join the sets 
                    self.union(l1, l2)
                    edges_added += 1

        # only one tree in the forest remaining now
        final_tree = self.Kforest[0]

        # get the vertex to make root
        r = final_tree.find(final_tree.root, self.get_vertex_from_label(self.start))
        final_tree.makeRoot(r, None)

        # save the final tree in the forest as the MST and add edges to traversed edges
        self.mst = final_tree
        self.addEdges(self.mst.root, False)


    # method to get the tree (set) belonging to a vertex with label l
    def getTree(self, l):
        v = self.get_vertex_from_label(l)
        for t in self.Kforest:
            if t.find(t.root, v): return t


    # join the two trees who have l1 and l2 as members
    def union(self, l1, l2):

        # get trees
        t1 = self.getTree(l1)
        t2 = self.getTree(l2)
        
        # if both were found join trees and remove one
        if t1 and t2:
            t1.placeTreeNodes(self.get_vertex_from_label(l1), self.get_vertex_from_label(l2), t2)
            del self.Kforest[self.Kforest.index(t2)]
            return True
        else:
            return False
                

    # method to serve as membership for sets
    def checkSameTree(self, l1, l2):
        return self.getTree(l1) == self.getTree(l2)
                    

    # calculate a MST with prims algorithm and get the preorder traversal for a tour
    # also using shortcutting to skip over previously visited vertices
    def calculatePrimsWithShortcut(self):

        # get MST from prims
        self.calculatePrims()

        # recalculate list of vertices
        self.verticesFromTree(self.mst.root)

        # add new list of edges using shortcutting to edges traversed
        self.shortcutEdges()


    # get a new list of edges based on the preoreder  list w/ backtracking of vertices
    def shortcutEdges(self):

        # get indices of vertices to skip by getting 
        # indices of items once they appear after the first time
        def duplicateIndices(l):
            p = []
            u = []
            for i in range(0, len(l) - 1):
                k = l[i]
                if k not in u:
                    u.append(k)
                else:
                    p.append(i)
            return p
            
        indicesToSkip = duplicateIndices(self.shortcutVisited)

        # refresh list from prims
        self.edgesTraversed = []

        # start at first vertex and go to second to last
        i = 0
        while i < len(self.shortcutVisited) - 1:

            # get current vertex
            cv = self.shortcutVisited[i]

            # get next vertex
            j = i + 1
            nv = self.shortcutVisited[j]

            # get adjoining edge
            e = self.edgeLabel(cv, nv)

            # while there exists a valid edge connecting current vertex and next vertex
            while(e and j in indicesToSkip):
                nv = self.shortcutVisited[j + 1]
                e = self.edgeLabel(cv, nv)
                
                # only increment j if a good edge was found
                if e: j += 1

            # add last good edge to traversed edges
            nv = self.shortcutVisited[j]
            e = self.edgeLabel(cv, nv)
            self.edgesTraversed.append(e)
            i = j


    # get an edge from two labels
    def edgeLabel(self, l1, l2):
        return self.getEdge(self.get_vertex_from_label(l1), self.get_vertex_from_label(l2))


    # get vertices from MST
    def verticesFromTree(self, v):
        self.shortcutVisited.append(v.data)
        for c in v.children:
            self.verticesFromTree(c)
            self.shortcutVisited.append(v.data)


    # calculate a MST with prims algorithm and get the preorder traversal for a tour
    def calculatePrims(self):

        # initialize each vertex root with distance 0
        self.MSTValues[self.get_vertex_from_label(self.start)] = 0

        # create min heap and tree data structure
        mh = MinHeapArray()
        nt = NTree()
        visited = []

        # insert vertices with initial distances into heap
        for t in self.MSTValues.items():
            mh.insert(t)

        # While there are unvisited vertices
        while not mh.isEmpty():
            t = mh.deleteMin()
            if t:
                cv = t[0]
            
                # don't add edge if it will create a cycle
                if cv not in visited:
                        
                    # add current vertex to visited
                    visited.append(cv)

                    # place vertex in MST
                    if cv.previousEdge:

                        # add previous (u, v) edge as new node u with parent v
                        nt.placeVertex(cv.previousEdge.label1, cv.previousEdge.label2)

                    # for each available edge
                    for e in self.openEdges(visited):

                        # calculate a new distance and relax each edge
                        new_dist = self.getEdgeCost(e) + self.MSTValues.get(cv)
                        nv = self.get_vertex_from_label(e.label2)
                        if nv:
                            if new_dist < self.MSTValues.get(nv):
                                mh.decreaseValue(nv, new_dist)
                                self.MSTValues[nv] = new_dist
                                nv.set_previous(cv)
                                nv.set_previous_edge(e)
        
        # get the MST
        self.mst = nt

        # add edges from MST in preorder traversal to traversed edges
        self.addEdges(self.mst.root, True)
        self.mst.preorder()


    # add edges to a list in preorder traversal with backtracking
    def addEdges(self, v, label_tree):
        
        l1 = v.data if label_tree else v.data.label
        
        # add edges for each children of V
        for c in v.children:
            l2 = c.data if label_tree else c.data.label
            e = self.getEdge(self.get_vertex_from_label(l1), self.get_vertex_from_label(l2))
            if e: 
                self.edgesTraversed.append(e)
                self.addEdges(c, label_tree)

        # add backtracking edge from V to parent
        if v.parent:
            parent_label = v.parent.data if label_tree else v.parent.data.label
            e = self.getEdge(self.get_vertex_from_label(l1), self.get_vertex_from_label(parent_label))
            if e: 
                self.edgesTraversed.append(e)


    # get generic cost of an edge based on time/ distance/ boarding
    def getEdgeCost(self, e):
        if self.time:
            if self.board:
                return self.getSkatingTimeSeconds(e)
            else:
                return self.getWalkingTimeSeconds(e)
        return e.length


    # get aviable edges from a list of vertices
    def openEdges(self, vertices):
        edges = []
        for v in vertices:
            adj_edges = self.get_adj_edges(v)
            for e in adj_edges:
                edges.append(e)
        return edges


    # calculate simple hamilton path using backtracking dfs
    def calculateHamiltonPath(self):

        # run backtracking dfs from start
        self.backtrackDFS(self.get_vertex_from_label(self.start))

        # check if all nodes were visited
        if len(self.visited) == len(self.vertices):
            return self.edgesTraversed
        return None


    # backtracking DFS algorithm to start at a particular vertex
    def backtrackDFS(self, start):

        # add vertex to visited
        self.visited.append(start)

        # for each adjacent vertex
        for v in self.get_adj_vertices(start):

            # if the adjacent vertex is unvisited
            if v not in self.visited:

                # add new edge, explore new node, add backtracking edge
                self.edgesTraversed.append(self.getEdge(start, v))
                self.backtrackDFS(v)
                self.edgesTraversed.append(self.getEdge(v, start))


    # get adjacent vertices
    def get_adj_vertices(self, vertex):
        adjs = []
        for e in self.edges:
            if e.label1 == vertex.label:
                adjs.append(self.get_vertex_from_label(e.label2))
        return adjs


    # get adjacent edges
    def get_adj_edges(self, vertex):
        adjs = []
        for e in self.edges:
            if e.label1 == vertex.label:
                adjs.append(e)
        return adjs


    # printout path of edges
    def printout_path(self, output_file):
        if self.edgesTraversed:
            legs = 0; distance = 0; time = 0
            for e in self.edgesTraversed:
                d, t = self.printEdge(e, output_file)
                legs += 1; distance += d; time += t
            print(f'legs = {legs}, distance = {distance} feet, time = {round(time/60, 1)} minutes', file = output_file)
        else:
            print('No such tour exists', file = output_file)


    # get edge with v1, v2
    def getEdge(self, v1, v2):
        if v1 and v2:
            for e in self.edges:
                if v1.label == e.label1 and v2.label == e.label2:
                    return e
        return None


    # print an edge
    def printEdge(self, e, output_file):
        v1 = self.get_vertex_from_label(e.label1)
        v2 = self.get_vertex_from_label(e.label2)
        print('FROM: (' + e.label1 + ') ' + str(v1), file = output_file)
        if e.name:
            print('ON: ' + e.name, file = output_file)
        print('Walk ' + str(e.length) + ' feet in direction ' + str(e.angle) + ' degrees ' + e.direction + '.', file = output_file)
        print('TO: (' + e.label2 + ') ' + str(v2), file = output_file)
        t = self.getEdgeTime(e)
        print('(' + str(t[0]) + ' ' + str(t[1]) + ')', file = output_file)
        print(file = output_file)
        if isinstance(t[0], float):
            return (e.length, round(t[0] * 60))
        return (e.length, t[0])


    # get time to traverse an edge
    def getEdgeTime(self, e):
        if self.board:
            return self.skatingTime(e)
        return self.walkingTime(e)


    # get vertex from label
    def get_vertex_from_label(self, label):
        if label:
            for v in self.vertices:
                if v.label == label:
                    return v
            for v in self.vertices:
                if label in v.name.lower().strip():
                    return v
            return None


    # get time to walk an edge
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


    # get time to walk an edge and conver to seconds or minutes
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