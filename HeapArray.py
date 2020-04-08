# @author Arjun Albert
# @email arjunalbert@brandeis.edu
# class to use for a min heap array data structure
class MinHeapArray:
    def __init__(self):
        self.heapArray = []
        self.nextElementIndex = 0


    # insert element (vertex, priority) into heap
    def insert(self, element):
        if isinstance(element, tuple):
            self.heapArray.insert(self.nextElementIndex, element)
            if element[1] < self.heapArray[self.parent(self.nextElementIndex)][1]:
                self.percup(self.nextElementIndex, self.parent(self.nextElementIndex))
            self.nextElementIndex += 1
        

    # switch an element at index with parent if heap conditions are not met
    def percup(self, index, parentIndex):
        self.swap(index, parentIndex)
        if self.heapArray[parentIndex][1] < self.heapArray[self.parent(parentIndex)][1]:
            self.percup(parentIndex, self.parent(parentIndex))

    
    # swap two elements in heap
    def swap(self, i1, i2):
        temp = self.heapArray[i1]
        self.heapArray[i1] = self.heapArray[i2]
        self.heapArray[i2] = temp
        

    # find vertex in heap
    def find(self, vertex):
        for t in self.heapArray:
            if t[0] == vertex and len(t) > 2:
                return t
        return None

     
    # test membership
    def member(self, vertex):
        return self.find(vertex) is not None


    # get index of vertex
    def indexOf(self, vertex):
        for x, y in enumerate(self.heapArray):
            if y[0] == vertex:
                return x
        return -1


    # decrease priority of value method for use in Dijkstra
    def decreaseValue(self, vertex, newValue):

        ti = self.indexOf(vertex)
        if ti != -1:

            # mark t as an invalid element
            t = self.heapArray[ti]
            if len(t) == 2:
                x, y = t
                self.heapArray[ti] = (x, y, "INVALID")

                # insert a new node with the correct value
                self.insert((vertex, newValue))


    # delete and return minimum element in heap
    def deleteMin(self):
        if self.nextElementIndex > 0:
            min_val = self.heapArray[0]
            self.swap(0, self.nextElementIndex - 1)
            del self.heapArray[self.nextElementIndex - 1]
            self.heapify(0)
            self.nextElementIndex -= 1

            # check for invalid elements and deleteMin again if so
            if len(min_val) > 2:
                return self.deleteMin()
            else:
                return min_val


    # ensure heap property holds from root down after delete
    def heapify(self, index):
        if index < len(self.heapArray):
            p = self.heapArray[index]; lc = self.lchild(index); rc = self.rchild(index)
            if rc >= len(self.heapArray):
                if not lc >= len(self.heapArray):
                    self.swap(index, lc)
            elif self.heapArray[rc][1] < self.heapArray[lc][1]:
                if p[1] > self.heapArray[rc][1]:
                    self.swap(index, rc)
                    self.heapify(rc)
            else:
                if p[1] > self.heapArray[lc][1]:
                    self.swap(index, lc)
                    self.heapify(lc) 


    # get parent index
    def parent(self, index):
        return int((index - 1) / 2)


    # get left child index
    def lchild(self, index):
        return (2 * index) + 1


    # get right child index
    def rchild(self, index):
        return (2 * index) + 2

    
    # check if heap is empty
    def isEmpty(self):
        return self.size() == 0


    # get how many elements are in the heap
    def size(self):
        num_valid = 0
        for t in self.heapArray:
            if len(t) == 2:
                num_valid += 1
        return num_valid


    # to string to be used for debugging
    def __str__(self):
        str_builder = ""
        for h in self.heapArray:
            if len(h) == 2:
                a, b = h
                str_builder += str(a) + " : " + str(b) + "\n"
        return str_builder


    # print to string for debugging
    def display(self):
        print(str(self))




    
