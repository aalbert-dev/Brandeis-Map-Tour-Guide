# @author Arjun Albert
# @email arjunalbert@brandeis.edu
# class for a N-ary tree node
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.children = []

    # add a node as this node's child
    def add_child(self, child):
        self.children.append(child)
        child.parent = self


    # replace child with same data element
    def replace_child(self, new_child):
        for c in self.children:
            if c.data == new_child.data:
                self.children[self.children.index(c)] = new_child
                return True
        return False