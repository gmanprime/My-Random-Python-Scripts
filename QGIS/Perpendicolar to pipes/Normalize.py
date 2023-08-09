from qgis.core import *
from qgis.gui import *
from pprint import pprint as pp
from numpy import arctan as tanInv, degrees as deg
project = QgsProject.instance()


class lineSegment:
    def __init__(self, vertex1, vertex2):
        nom = (vertex2.y() - vertex1.y())
        denom = (vertex2.x() - vertex1.x())
        if denom == 0:
            denom = 0.00001

        self.m = nom/denom
        self.b = vertex1.y() - (self.m * vertex1.x())

    def intersects(self, vertex):
        vertex = vertex.geometry().asPoint() if type(vertex) != QgsPoint else None

        Fx = (self.m * vertex.x()) + self.b

        if (round(vertex.y(), 4) == round(Fx, 4)):
            return True
        else:
            return False

    def slope(self):
        return self.m


def normAngle(layerName, feature):
    global lines, line, vertices

    # Get all the line features in the layer.
    lines = project.mapLayersByName(layerName)[0]

    # Note: This seems to work in the function editor
    geom = feature.geometry().buffer(0.1, 8)

    # Iterate over the line features.
    for line in lines.getFeatures():
        # Check if the line feature intersects the point feature currently being analized.
        if line.geometry().intersects(geom):
            # The line feature intersects the point, so return it.
            lines.removeSelection()
            lines.select(line['fid'])
            break

    # get vertices from line element

    Nodes = []

    vertices = line.geometry().vertices()
    vertices = list(vertices)
    angle = 0

    for i, vertex in enumerate(vertices):
        if i < len(vertices)-1:
            segment = lineSegment(vertex, vertices[i+1])

            if (segment.intersects(feature)):
                m = segment.slope()
                angle = deg(tanInv(m))

    feature.setAttribute("ROTATION", angle)
    return angle - 90


#########################################################################
endCaps = project.mapLayersByName('End Cap')[0]
for cap in endCaps.getFeatures():
    normAngle('Miya Pipes V2 July 21', cap)
# selectedCaps = list(endCaps.getSelectedFeatures())
# vertices = normAngle('Miya Pipes V2 July 21', selectedCaps[0])
# print(vertices)
