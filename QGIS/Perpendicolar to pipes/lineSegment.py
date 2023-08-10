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
