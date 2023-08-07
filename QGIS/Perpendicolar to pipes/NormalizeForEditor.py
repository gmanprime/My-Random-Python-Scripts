from qgis.core import *
from qgis.gui import *
from pprint import pprint as pp
from numpy import arctan as tanInv, degrees as deg
project = QgsProject.instance()


class lineSegment:
    def __init__(self, startPoint, endPoint):
        # Define a delta y and xvalue as the nominator and denominator values
        denom = endPoint.x() - startPoint.x()
        nom = endPoint.y() - startPoint.y()

        # calculate the class wide slope value for the line Segment from the nom denom values
        self.m = nom/denom

        # calculate the Y intercept for the line segment from the slope and starting point
        self.b = startPoint.y() - (self.m * startPoint.x())

    def intersects(self, feat):
        """
        function that computest weather a point Feature intersects the line segment

        Args:
            feat (QgsFeature): point feature to conclude intersection with

        Returns:
            Bool: True or false for intersection test
        """

        # check weather the feature is QgsFeature type first
        # convert the QgsFeature type to point type
        if type(feat) == QgsFeature:
            feat = feat.geometry().asPoint()

            # compute line y value at the points x value
            Fx = (self.m * feat.x()) + self.b

            # check weather the line segment and point are within a small tolerance of eachother
            if (round(feat.y(), 4) == round(Fx, 4)):
                return True
            else:
                return False

    def slope(self):
        return self.m


@qgsfunction(group='Custom', referenced_columns=[])
def normAngle2(layerName, feature, parent):
    print(feature)
    global lines, line, vertices

    # Get all the line features in the layer.
    lines = project.mapLayersByName(layerName)[0]

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

    return angle
