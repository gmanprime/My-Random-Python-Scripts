import processing
import random
import string
from pprint import pprint as pp
from qgis.core import QgsProject, QgsProcessing

# *********************************************************
# get the active polygon layer
dmaBoundary = QgsProject.instance().mapLayersByName('DMA_Boundary_V3')[0]

# get the raster layer
rasterLayer = QgsProject.instance().mapLayersByName('Addis_Ababa_Elevation')[0]


def alphaNumGen(size=8):
    # get letters as a list
    letters = string.ascii_lowercase + string.digits
    # return a random string of chars
    return ''.join(random.choice(letters) for i in range(size))


# *********************************************************
# create a point layer from the values of the raster layer
pointLayer = processing.run("native:pixelstopoints", {
    'INPUT_RASTER': rasterLayer,
    'RASTER_BAND': 1,
    'FIELD_NAME': 'elevation',
    'OUTPUT': 'TEMPORARY_OUTPUT'
})

# *********************************************************
# join the point layer to the original polygon layer
# This layer contains point features that have all the altitude data laid out in a point grid.
# From this we can find the points with the smallest and highest elevation value.
# And from the min and max values, we can then find the average altitude and the point closest to that average value

joinedLayer = processing.run("native:joinattributesbylocation", {
    'INPUT': pointLayer['OUTPUT'],
    'PREDICATE': [0],
    'JOIN': dmaBoundary,
    'JOIN_FIELDS': ['DMA'],
    'METHOD': 0,
    'DISCARD_NONMATCHING': True,
    'PREFIX': '',
    'OUTPUT': 'TEMPORARY_OUTPUT'
})

testFeatures = []

# Create a new field called "id" and add it to joinedLayer layer
xid = QgsField("xid", QVariant.String)
joinedLayer['OUTPUT'].dataProvider().addAttributes([xid])

# update fields for the joinedlayer in order to get changes from above
joinedLayer['OUTPUT'].updateFields()

for i, feature in enumerate(joinedLayer['OUTPUT'].getFeatures()):
    feature.setAttribute('xid', alphaNumGen(8))
    joinedLayer['OUTPUT'].updateFeature(feature)
    if i >= 5 and i <= 10:
        testFeatures.append(feature)
        print(feature.attributes())


# Commit the changes
joinedLayer['OUTPUT'].commitChanges()

# complete: need to create a random ID generator for the joinedlayer id


# Add the converted geoLayer to the project for visibility
# Note: toggle the below line to print out joinedLayer to the map
QgsProject.instance().addMapLayer(joinedLayer['OUTPUT'])

# *********************************************************
# classify features based on DMA
# what this section basically does is take each feature out of the vector geoLayer "vectorJoinedLayer" and
# then adds it to a dictionary to be classified by DMA

dmaDict = {}  # create a dictionary that will hold the data classified further by using DMA's as key classifiers

# classify every feature
# ? might be a source of error
for feature in joinedLayer['OUTPUT'].getFeatures():
    dma = feature["DMA"]

    # checks to see if the DMA already exists in the dmaDict dictionary
    # and if not, adds it as a possible empty list
    if dma not in dmaDict:
        dmaDict[dma] = []

    # this proceeds to add the current feature to the dictionary variable
    dmaDict[dma].append(feature)

# *********************************************************
# this section find the features with the biggest and smallest elevation values
# outputFeatures is the variable where these features are put
outputFeatures = []

# this function can be used to make new features similar in pattern to the above layers

for dma in dmaDict:
    minFeature = min(dmaDict[dma], key=lambda f: f['elevation'])
    maxFeature = max(dmaDict[dma], key=lambda f: f['elevation'])

    # find the feature with the closest elevation to the mean
    meanElevation = sum([f['elevation']
                        for f in dmaDict[dma]]) / len(dmaDict[dma])

    avgFeature = min(dmaDict[dma], key=lambda f: abs(
        f['elevation'] - meanElevation))

    # create a new feature with the min, max, and average elevation values
    outputFeatures.extend([minFeature, maxFeature, avgFeature])

# Create a new layer from the list of features
minMaxLayer = QgsVectorLayer("Point?crs=EPSG:20137&memory",
                             "min max layer", "memory")

# Add the features to the layer
minMaxLayer.dataProvider().addAttributes(joinedLayer['OUTPUT'].fields())

# Update the layer schema
minMaxLayer.updateFields()

# for feature in outputFeatures:
#     minMaxLayer.dataProvider().addFeature(feature)

minMaxLayer.dataProvider().addFeatures(outputFeatures)

# # Add the layer to the current project
QgsProject.instance().addMapLayer(minMaxLayer)
