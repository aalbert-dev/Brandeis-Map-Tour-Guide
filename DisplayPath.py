# @author Arjun Albert
# @email arjunalbert@brandeis.edu
# class to display paths on the brandeis map
# import PIL soley for displaying images in python
# I import PIL an external python package so I 
# can test and debug my classes - nothing data
# structure related

# also if other classes are erroring as a result of importing this class
# please uncomment those lines and rerun any tests
from PIL import Image, ImageDraw
import Constraints
class DisplayPath:

    # create a class to dipslay a path on the brandeis map
    def __init__(self, edges, all_vertices):
        self.edges = edges
        self.all_vertices = all_vertices
        
    
    # draw the path on the image file
    def draw(self):
        print()
        map_im = Image.open('BrandeisMapLabeledCropped.jpg')
        color = (0, 20, 240); color_range = 255 * 2; color_mod = int(color_range / len(self.edges))
        if color_mod == 0: color_mod = 1
        
        # add each edge as a line on the map, changing color values at every iteration
        for e in self.edges:
            color = self.mod_color(color, color_mod)
            self.draw_edge(e, map_im, color)

        # show the map
        map_im.show()


    # modify a RGB color tuple
    def mod_color(self, color, cm):
        if color[0] < 255:
            return (color[0] + cm, color[1], color[2])
        elif color[1] < 255:
            return (color[0], color[1] + cm, color[2])
        elif color[2] < 255:
            return (color[0], color[1], color[2] + cm)
        else:
            return color
    

    # get coordinates of a vertex
    def vertex_coordinates(self, label):
        for v in self.all_vertices:
            if v.label == label:
                return (v.x, v.y)


    # get coordinates of an edge
    def edge_coordinates(self, edge):
        return (self.vertex_coordinates(edge.label1), self.vertex_coordinates(edge.label2))


    # draw an edge given coordinates
    def draw_edge(self, edge, img, color):
        draw = ImageDraw.Draw(img)
        v1, v2 = self.edge_coordinates(edge)
        x1, y1 = v1
        x2, y2 = v2
        #f  = c * MapHeightPixels / MapHeightFeet - cropDirection
        p1 = (x1 * Constraints.MapHeightPixels / Constraints.MapHeightFeet)  - Constraints.CropLeft
        p2 = (y1 * Constraints.MapHeightPixels / Constraints.MapHeightFeet) - Constraints.CropDown
        p3 = (x2 * Constraints.MapHeightPixels / Constraints.MapHeightFeet) - Constraints.CropLeft
        p4 = (y2 * Constraints.MapHeightPixels / Constraints.MapHeightFeet) - Constraints.CropDown
        # print(int(p1), int(p2), int(p3), int(p4))
        draw.line((p1, p2, p3, p4), fill=(color[0], color[1], color[2]), width = 4)