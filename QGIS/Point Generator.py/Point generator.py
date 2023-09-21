'''
This QGIS python code will take in selected points from one layer
and create duplicate points in an already existing database layer
'''

import random
from pprint import pprint as pp

from qgis.core import QgsProject, QgsVectorLayer


class pointRegen:
    def __init__(self, sourceLayerName, targetLayerName, filter=None):

        # sourceLayer => Layer from which point is extracted
        self.sourceLayer = QgsProject.instance(
        ).mapLayersByName(sourceLayerName)[0]

        # targetLayer => Layer to which the feature is being copied
        self.targetLayer = QgsProject.instance(
        ).mapLayersByName(targetLayerName)[0]

        self.targetLayer.startEditing()

        self.sourceFeatIterator = self.sourceLayer.getFeatures()
        self.sourceFeatures = list(self.sourceFeatIterator)
        self.sampleList = []

    def sample(self, length, sourceList=[]):
        # generate a sample list stored internally
        # this is to be used for optional subgroup processing

        if self.sourceFeatures is None:
            self.sourceFeatures = list(self.sourceLayer.getFeatures())

        if sourceList == []:
            self.currentSample = random.sample(self.sourceFeatures, length) if length < len(
                self.sourceFeatures) else None
            self.sampleList.append(self.currentSample)
            return self.currentSample
        else:
            self.currentSample = random.sample(sourceList, length) if length > len(
                sourceList) else None
            self.sampleList.append(self.currentSample)
            return self.currentSample

    def clearSamples(self, clearOld=False):
        self.currentSample = []
        if clearOld == True:
            self.sampleList = []

    def transmuteAttrivs(self, updateMap: dict):
        pass

    def duplicator(self, sourceFeatures):
        """Duplicates the given source features.

        Args:
            sourceFeatures: A list of QgsFeature objects.

        Returns:
            A tuple of (validFeatures, invalidFeatures, isAllValid), where:
                validFeatures: A list of QgsFeature objects that were successfully duplicated.
                invalidFeatures: A list of QgsFeature objects that could not be duplicated.
                isAllValid: A boolean value indicating whether all of the source features were successfully duplicated.
        """

        # Create two lists to store the valid and invalid features.
        self.validFeats = []
        self.invalidFeats = []

        # Check variable for weather the feature is valid.
        areAllValid = True

        for feature in sourceFeatures:

            if feature.isValid():
                # Create a new feature and copy the geometry from the source feature.
                newFeat = QgsFeature()
                newFeat.setGeometry(feature.geometry())

                # Note: This is where the features attributes should be updated.

                self.validFeats.append(newFeat)

            else:
                # Add the invalid feature to the list of invalid features.
                self.invalidFeats.append(feature)
                areAllValid = False

        # Return the valid and invalid features, as well as a boolean value indicating whether all of the source features were successfully duplicated.
        return self.validFeats, self.invalidFeats, areAllValid

    def updateTarget(self, features):
        """
        Updates the map with the given features.

        Args:
            features: A list of QgsFeature objects.

        Returns:
            True if all features were successfully added to the map, False otherwise.
        """

        # iterate over list of features and classify
        validFeats, invalidFeats, areAllValid = self.duplicator(features)
        pp(validFeats)

        # raise and error if there are invalid features
        if not areAllValid:
            raise ValueError("The following features are invalid: {}".format(
                ", ".join(str(f.id()) for f in invalidFeats)))

        # add valid features to map if error passes
        self.targetLayer.dataProvider().addFeatures(validFeats)

        return areAllValid

    def clearTargetFields(self, clearList=[]):
        # first clear all fields if no fields are defined
        if clearList == []:
            fields = self.targetLayer.fields()
            for field in fields:
                self.targetLayer.deleteField(field.index())
        else:
            for field in clearList:
                self.targetLayer.dataProvider().deleteField(field.index())

    def updateTargetFields(self):
        # the updateMap can be used to match differently named fields
        self.targetFields = self.targetLayer.fields()
        self.sourceFields = self.sourceLayer.fields()
        targetFieldNames = self.targetFields.names()

        fieldsToAdd = []

        for field in self.sourceFields:
            if field.name() not in targetFieldNames:
                fieldsToAdd.append(field)

        self.targetLayer.dataProvider().addAttributes(fieldsToAdd)
        self.targetLayer.updateFields()

    def main(self):
        # Main executable function
        pass


gen = pointRegen('VALVE_MIYA', 'testTable1')
