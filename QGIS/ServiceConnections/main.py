class ServiceConnection:
    def __init__(self, ptL1Name, ptL2Name):
        self.ptLayer1 = QgsProject.instance().mapLayersByName(ptL1Name)[0]
        self.ptLayer2 = QgsProject.instance().mapLayersByName(ptL2Name)[0]

        self.l1Feats = self.ptLayer1.getFeatures()
        self.l2Feats = self.ptLayer2.getFeatures()

        self.lineLayer = QgsVectorLayer('LineString', 'MyLineLayer', 'memory')
        return None

    def featuresAsPoints(self, features):
        points = []
        for feature in features:
            px = feature.geometry().asPoint().x()
            py = feature.geometry().asPoint().y()

            points.append(QgsPoint(px, py))
        return points

    def makeLine(self, pt1: QgsPoint, pt2: QgsPoint) -> QgsFeature:
        lineGeom = QgsGeometry.fromPolyline(
            [
                pt1,
                pt2,
            ]
        )
        outFeature = QgsFeature(self.lineLayer.fields())
        outFeature.setGeometry(lineGeom)

        return outFeature

    def mapLines(self, features):
        lineLayer.dataProvider().addFeatures(features)
        lineLayer.commitChanges()
        QgsProject.instance().addMapLayer(self.lineLayer)

        return None

    def Main(self):
        pass


sc = ServiceConnection('CM_08112023', 'CUSTOMER_08112023')
