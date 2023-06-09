import processing
import random
import string
from pprint import pprint as pp
from qgis.core import QgsProject, QgsProcessing, QgsVectorLayer, QgsField


class altRanger():
    """
    Class to calculate the minimum, maximum, and average elevation for each polygon grouping in a raster layer.

    Args:
        raster: The raster layer containing elevation data.
        boundary: The vector layer containing DMA boundaries.
        bfld: The name of the field in the boundary layer that contains the DMA IDs.
    """

    def __init__(self, raster, boundary, bfld):
        """
        Create a new altRanger object.

        Args:
            raster: The raster layer containing elevation data.
            boundary: The vector layer containing DMA boundaries.
            bfld: The name of the field in the boundary layer that contains the DMA IDs.
        """
        # Convert the raster layer to a point layer.
        self.zLayer = self._zPoints(raster)

        # Set the class variables.
        self.bfld = bfld
        self.minmaxFeatures = []
        self.outputFeatures = []
        self.groups = {}
        self.layer = self._joinLayers(self.zLayer, boundary, [bfld])
        self.minmaxLayer = self._genMinMaxLayer()

    def printArr(self, arr):
        """
        Print the contents of an array.

        Args:
            arr: The array to print.
        """
        for item in arr:
            pp(item)

    def _alphaNumGen(self, size=8):
        """
        Generate a random alphanumeric string of the specified length.

        Args:
            size: The length of the string to generate.

        Returns:
            The generated string.
        """
        # get letters as a list
        letters = string.ascii_lowercase + string.digits
        # return a random string of chars
        return ''.join(random.choice(letters) for i in range(size))

    def _zPoints(self, raster):
        """
        Create a point layer from a raster layer.

        Args:
            raster: The raster layer to convert.

        Returns:
            The created point layer.
        """
        return processing.run("native:pixelstopoints", {
            'INPUT_RASTER': raster,
            'RASTER_BAND': 1,
            'FIELD_NAME': 'elevation',
            'OUTPUT': 'TEMPORARY_OUTPUT'
        })['OUTPUT']

    def _joinLayers(self, zLayer, Boundary, fields=[]):
        """
        Join two layers based on geolocation intersection

        Args:
            zLayer: The first layer to join.
            Boundary: The second layer to join.
            fields: The names of the fields to join on.

        Returns:
            The joined layer.
        """
        # Print the arguments to the function.
        self.printArr([zLayer, Boundary, fields])

        # Join the layers.
        joinedLayer = processing.run("native:joinattributesbylocation", {
            'INPUT': zLayer,
            'PREDICATE': [0],
            'JOIN': Boundary,
            'JOIN_FIELDS': fields,
            'METHOD': 0,
            'DISCARD_NONMATCHING': True,
            'PREFIX': '',
            'OUTPUT': 'TEMPORARY_OUTPUT'
        })

        # Create a new field called "xid" and add it to joinedLayer layer
        xid = QgsField("xid", QVariant.String)
        joinedLayer['OUTPUT'].dataProvider().addAttributes([xid])

        # update fields for the joinedlayer in order to get changes from above
        joinedLayer['OUTPUT'].updateFields()

        # Iterate over the features in the joined layer and assign them a random ID.
        for i, feature in enumerate(joinedLayer['OUTPUT'].getFeatures()):
            feature.setAttribute('xid', self._alphaNumGen(8))
            joinedLayer['OUTPUT'].updateFeature(feature)

        # Commit the changes to the joined layer.
        joinedLayer['OUTPUT'].commitChanges()

        # Return the joined layer.
        return joinedLayer['OUTPUT']

    def _groupByBoundary(self):
        """
        Groups the features in the layer by their groups ID.

        The groups are stored in a dictionary, where the key is the DMA ID and the value is a list of features with that ID.
        """
        # Initialize the groups dictionary.
        groups = self.groups

        # Iterate over the features in the layer.
        for feature in self.layer.getFeatures():
            # Get the group ID from the feature.
            groupID = feature[self.bfld]

            # If the group ID is not in the groups dictionary, create a new list for it.
            if groupID not in groups:
                groups[groupID] = []

            # Add the feature to the list for the DMA ID.
            groups[groupID].append(feature)

    def _genMinMaxVals(self):
        """
        Calculates the minimum, maximum, and average elevation for each group of features.

        The results are stored in a dictionary, where the key is the groups ID and the value is a tuple of the minimum, maximum, and average elevation.
        """

        # Initialize the groups dictionary.
        groups = self.groups

        # Initialize the minMaxData dictionary.
        minMaxData = {
            'min': [],
            'max': [],
            'avg': []
        }

        # Iterate over the available groups in grouped features.
        for groupID in groups:

            # Find the minimum elevation in the group.
            minFeature = min(groups[groupID],
                             key=lambda f: f['elevation'])

            # Find the maximum elevation in the group.
            maxFeature = max(groups[groupID],
                             key=lambda f: f['elevation'])

           # Calculate the average elevation in the group.
            meanElevation = sum([f['elevation']
                                for f in groups[groupID]]) / len(groups[groupID])

            # find the feature closest to the average elevation value
            avgFeature = min(groups[groupID], key=lambda f: abs(
                f['elevation'] - meanElevation))

            # Add the minimum, maximum, and average elevation to the minMaxData dictionary.
            minMaxData['min'].append(minFeature)
            minMaxData['max'].append(maxFeature)
            minMaxData['avg'].append(avgFeature)

            # create a new feature with the min, max, and average elevation values
            self.outputFeatures.extend([minFeature, maxFeature, avgFeature])

        return minMaxData

    def _genMinMaxLayer(self):
        """
        Create a new layer containing the minimum, maximum, and average elevation for each DMA.

        The new layer has the same crs as the input layer.
        """
        # Get the fields from the input layer.
        layer = self.layer
        outputFeatures = self.outputFeatures

        # Create a new layer from the list of features
        minMaxLayer = QgsVectorLayer(
            "Point?crs=EPSG:32637&memory", "minmax layer", "memory")

        # Add the features to the layer
        minMaxLayer.dataProvider().addAttributes(
            layer.fields())

        # Update the layer schema
        minMaxLayer.updateFields()

        minMaxLayer.dataProvider().addFeatures(outputFeatures)

        return minMaxLayer

    def mapLayers(self):
        layer = self.layer
        minmaxLayer = self.minmaxLayer

        if (layer):
            # add Layers to map after commit
            QgsProject.instance().addMapLayer(layer)

        if (minmaxLayer):
            # Add the layer to the current project
            QgsProject.instance().addMapLayer(minmaxLayer)


def main():
    # get raster and boundary layer
    dmaBoundary = QgsProject.instance().mapLayersByName('DMA_Boundary_V3')[0]
    rasterLayer = QgsProject.instance().mapLayersByName(
        'Addis_Ababa_Elevation')[0]

    # create a ranger object for computing min max and average values
    rng = altRanger(rasterLayer, dmaBoundary, 'DMA')

    # add the resulting layers to map
    rng.mapLayers()

    # check the validity of the ranger object rng
    print(rng)


main()  # run everything
