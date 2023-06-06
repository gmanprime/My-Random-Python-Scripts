# Get the active polygon layer.
dmaBoundary = QgsProject.instance().mapLayersByName('DMA_Boundary_V3')[0]

# Get the raster layer.
rasterLayer = QgsProject.instance().mapLayersByName('Addis_Ababa_Elevation')[0]

# Create a point layer from the values of the raster layer.
# This layer will contain point features that have all the altitude data laid out in a point grid.
# We can then use this layer to find the points with the smallest and highest elevation value,
# as well as the average altitude and the point closest to that average value.
pointLayer = processing.run("native:pixelstopoints", {
    'INPUT_RASTER': rasterLayer,
    'RASTER_BAND': 1,
    'FIELD_NAME': 'elevation',
    'OUTPUT': 'TEMPORARY_OUTPUT'
})

# Join the point layer to the original polygon layer.
# This will create a new layer that contains all of the features from the point layer,
# as well as the corresponding DMA values from the original polygon layer.
# This will allow us to classify the features based on DMA.
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

# Add the converted geoLayer to the project for visibility.
QgsProject.instance().addMapLayer(joinedLayer['OUTPUT'])

# Create a dictionary that will hold the data classified further by using DMA's as key classifiers.
dmaDict = {}

# Classify every feature.
for feature in joinedLayer['OUTPUT'].getFeatures():
    dma = feature["DMA"]  # Get DMA value of the current feature.

    # Check to see if the DMA already exists in the dmaDict dictionary.
    # If not, add it as a possible empty list.
    if dma not in dmaDict:
        dmaDict[dma] = []

    # Add the current feature to the dictionary variable.
    dmaDict[dma].append(feature)

# Find the features with the biggest and smallest elevation values.
# The outputFeatures variable will hold these features.
outputFeatures = []

# This function can be used to make new features similar in pattern to the above layers.

for dma in dmaDict:
    minFeature = min(dmaDict[dma], key=lambda f: f['elevation'])
    maxFeature = max(dmaDict[dma], key=lambda feature: feature['elevation'])

    # Find the feature with the closest elevation to the mean.
    meanElevation = sum([f['elevation']
                        for f in dmaDict[dma]]) / len(dmaDict[dma])

    avgFeature = min(dmaDict[dma], key=lambda f: abs(
        f['elevation'] - meanElevation))

    # Create a new feature with the min, max, and average elevation values.
    outputFeatures.extend([minFeature, maxFeature, avgFeature])

# Create a new layer from the list of features.
minMaxLayer = QgsVectorLayer("Point?crs=EPSG:20137&memory",
                             "min max layer", "memory")

# Add the features to the layer.
minMaxLayer.dataProvider().addAttributes(joinedLayer['OUTPUT'].fields())

# Update the layer schema.
minMaxLayer.updateFields()

# Add the features to the layer.
minMaxLayer.dataProvider().addFeatures(outputFeatures)

# Add the layer to the current project.
QgsProject.instance().addMapLayer(minMaxLayer)
