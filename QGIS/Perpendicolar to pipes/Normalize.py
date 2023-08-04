from qgis.core import *
from qgis.gui import *

project = QgsProject.instance()


class Node:
    def __init__(self, data, preNext=None, prePrev=None) -> None:
        self.data = data
        self.next = preNext
        self.prev = prePrev

    def append(self, newNode):
        if type(newNode) == Node:
            oldNext = self.next                 # extract the old next
            self.next = newNode           # set current next to a new Node element
            if oldNext:
                # set the previous element of the old next to the new next element
                oldNext.prev = self.next
            self.next.next = oldNext            # append the old next element to the new node
            # set the previous value of the new element to the current node
            self.next.prev = self
            return newNode
        else:
            print("Not a node type element")

    def prepend(self, newNode):
        oldPrev = self.prev                 # extract the old prev
        self.prev = newNode              # set current prev to a new Node element
        if oldPrev:
            # set the previous element of the old prev to the new prev element
            oldPrev.next = self.prev
        self.prev.prev = oldPrev            # append the old next element to the new node
        # set the previous value of the new element to the current node
        self.prev.next = self

    def delete(self):
        if self.next:
            self.next.prev = self.prev
        if self.prev:
            self.prev.next = self.next
        self.next = None
        self.prev = None
        self.data = None

    def view(self):
        print(f'prev: {self.prev.data if self.prev else self.prev}')
        print(f'node: {self.data}')
        print(f'next: {self.next.data if self.next else self.next}')
        print('\n')

    def viewFollowing(self):
        if self.next == None:
            return
        else:
            self.next.view()
            self.next.viewFollowing()

    def viewPreceding(self):
        if self.prev == None:
            self.view()
        else:
            self.prev.viewPreceding()


def normAngle(layerName, feature):
    global lines, line, rawVertices
    # Get all the line features in the layer.
    lines = project.mapLayersByName(layerName)[0]

    intLine = None
    geom = feature.geometry().buffer(0.1, 8)

    # Iterate over the line features.
    for line in lines.getFeatures():
        # Check if the line feature intersects the point feature currently being analized.
        if line.geometry().intersects(geom):
            # The line feature intersects the point, so return it.
            intLine = line
            break

    # get vertices from line element
    lines.removeSelection()
    lines.select(line['fid'])

    Nodes = []

    for i, vertex in enumerate(line.geometry().vertices()):
        # !: this is wheer we need to edit
        pass

    rawVertices = line.geometry().vertices()
    vertices = [vertex for vertex in rawVertices]

    # extract x,y values for the vertecies
    xy_values = [{'x': vertex.x(), 'y': vertex.y()} for vertex in vertices]

    return xy_values


#########################################################################
endCaps = project.mapLayersByName('End Cap')[0]
selectedCaps = list(endCaps.getSelectedFeatures())
vertices = normAngle('Miya Pipes V2 July 21', selectedCaps[0])
print(vertices)
