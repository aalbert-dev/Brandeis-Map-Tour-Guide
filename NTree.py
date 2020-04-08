# @author Arjun Albert
# @email arjunalbert@brandeis.edu
# class for an N-ary tree to hold map vertices
from Node import TreeNode
class NTree:
    def __init__(self):
        self.root = None
        self.num_nodes = 0
        self.backtrack_preorder = []
        self.marked_vertices = []
    

    # add a root
    def addRootVertex(self, v):
        n = TreeNode(v)
        self.root = n
        self.num_nodes += 1


    # place ith vertex as child of parent
    def placeVertex(self, parent_data, child_data):

        # place root and first child if first node
        if self.num_nodes == 0:
            self.addRootVertex(parent_data)
            self.placeVertex(parent_data, child_data)
            return True

        # place vertex elsewhere
        else:
            result = self.find(self.root, parent_data)
            if result: 
                n = TreeNode(child_data)
                result.add_child(n)
                self.num_nodes += 1
                return True


    # join two trees 
    def joinTree(self, other):
        otherRoot = other.root
        result = self.find(self.root, otherRoot.data)
        if result and result.parent: 
            result.parent.replace_child(otherRoot)
            self.num_nodes += (other.num_nodes - 1)
            return True
        return False


    # place a new node as a child of it's parent
    def placeTreeNodes(self, parent_data, child_data, otherTree):
        v1 = self.find(self.root, parent_data); v2 = otherTree.find(otherTree.root, child_data)

        # if v2 is the root append, otherwise make v2 the root and append
        if not v2.parent:
            v1.add_child(v2)
        else:
            otherTree.makeRoot(v2, None)
            v1.add_child(v2)
        self.num_nodes += otherTree.num_nodes


    # make a node the new root of this tree
    def makeRoot(self, v, prev):

        # mark as root if there is no parent
        if not prev:
            self.root = v
        
        # traverse up the tree to the root reassigning parent pointers
        keep_parent = v.parent
        if keep_parent:
            del keep_parent.children[keep_parent.children.index(v)]
            v.parent = prev
            v.children.append(keep_parent)
            self.makeRoot(keep_parent, v)
        else:
            v.parent = prev


    # print out child, parent relationship for each node for debugging
    def print_parents(self):
        for v in self.preorder():
            print(v.data, str(v.parent.data if v.parent else v.parent))

            
    # find a vertex with label l
    def find(self, v, l):
        if v.data == l:
            return v
        else:
            for c in v.children:
                r = self.find(c, l)
                if r:
                    return r


    # get size of tree
    def size(self):
        return self.num_nodes


    # preorder travesal starting with root, returns order of visited nodes
    def preorder(self):
        self.marked_vertices = []
        self.preorder_util(self.root)
        return self.marked_vertices


    # recursive preorder method 
    def preorder_util(self, v):
        self.marked_vertices.append(v)
        for c in v.children:
            self.preorder_util(c)
            self.marked_vertices.append(v)


    # to string
    def __str__(self):
        sb = ''
        for v in self.preorder():
            sb += str(v.data) + '\n'
        return sb