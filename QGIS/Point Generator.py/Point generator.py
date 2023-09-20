'''
This QGIS python code will take in selected points from one layer
and create duplicate points in an already existing database layer
'''

import random

from qgis.core import QgsProject, QgsVectorLayer


class pointRegen:
    def __init__(self, sourceLayerName, targetLayerName, filter=None):

        # sourceLayer => Layer from which point is extracted
        self.sourceLayer = QgsProject.instance(
        ).mapLayersByName(sourceLayerName)[0]

        # targetLayer => Layer to which the feature is being copied
        self.targetLayer = QgsProject.instance(
        ).mapLayersByName(targetLayerName)[0]

        self.sourceFeatIterator = self.sourceLayer.getFeatures()
        self.sourceFeatures = list(self.sourceFeatIterator)

    def sample(self, length, sourceList=[]):
        # generate a sample list stored internally
        # this is to be used for optional subgroup processing

        if self.sourceFeatures is None:
            self.sourceFeatures = list(self.sourceLayer.getFeatures())

        if sourceList == []:
            return random.sample(self.sourceFeatures, length) if length < len(
                self.sourceFeatures) else None
        else:
            return random.sample(sourceList, length) if length > len(
                sourceList) else None

    def replicateAttributes(self):
        pass

    def duplicator(self, sourceFeatures: list):

        newFeats = []

        for feat in sourceFeatures:
            newFeat = Feature()
            newFeat.setGeometry(feat.geometry())
            newFeats.append(newFeat)

        # takes in a point and creates a duplicate
        return


generator = pointRegen('VALVE_MIYA', 'testTable1')
