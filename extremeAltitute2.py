import processing
from pprint import pprint as pp
from qgis.core import QgsProject, QgsProcessing

# *********************************************************
# get the active polygon layer
dmaBoundary = QgsProject.instance().mapLayersByName('DMA_Boundary_V3')[0]

# get the raster layer
rasterLayer = QgsProject.instance().mapLayersByName('Addis_Ababa_Elevation')[0]

# *********************************************************
# create a point layer from the values of the raster layer
pointLayer = processing.run("native:pixelstopoints", {
    'INPUT_RASTER':rasterLayer,
    'RASTER_BAND':1,
    'FIELD_NAME':'elevation',
    'OUTPUT': 'pointLayer'
    })

# *********************************************************
# join the point layer to the original polygon layer

joinedLayer = processing.run("native:joinattributesbylocation", {
    'INPUT': pointLayer['OUTPUT'],
    'PREDICATE':[0],
    'JOIN':dmaBoundary,
    'JOIN_FIELDS':['DMA'],
    'METHOD':0,
    'DISCARD_NONMATCHING':True,
    'PREFIX':'',
    'OUTPUT':'joinedLayer'
    })


vectJoinedLayer = QgsVectorLayer(joinedLayer['OUTPUT'], "joinedLayer", "ogr")
QgsProject.instance().removeMapLayer(vectJoinedLayer)#removes joined layer from map
QgsProject.instance().addMapLayer(vectJoinedLayer)

# *********************************************************
#classify features based on DMA

dmaDict = {} #create a dictionary with dma key values

#classify every feature
for feature in vectJoinedLayer.getFeatures():
    dma = feature["DMA"] #get DMA value
    
    #add DMA classification to dictionary if DMA does not exists
    if dma not in dmaDict:
        dmaDict[dma] = []
    
    #add feature to dicitionary
    dmaDict[dma].append(feature)
    
# *********************************************************
# find the features with the biggest and smallest elevation values

outputFeatures = []

def makeFeat(dma, elevation, stat):
    feat = QgsFeature()
    feat.addFields([
        QgsField("DMA", QVariant.Int),
        QgsField("elevation", QVariant.Int),
        QgsField("stat", QVariant.Int),
        ])
    
    feat['DMA'] = dma
    feat['elevation'] = minFeature['elevation']
    feat['stat'] = 'min'
    return feat

for dma in dmaDict:
    minFeature = min(dmaDict[dma], key=lambda f: f['elevation'])
    maxFeature = max(dmaDict[dma], key=lambda f: f['elevation'])

    # find the feature with the closest elevation to the mean
    meanElevation = sum([f['elevation'] for f in dmaDict[dma]]) / len(dmaDict[dma])
    avgFeature = min(dmaDict[dma], key=lambda f: abs(f['elevation'] - meanElevation))

    # create a new feature with the min, max, and average elevation values
    outputFeatures.extend([minFeature, maxFeature, avgFeature])
    
pp(outputFeatures[0])
    
# Create a new layer from the list of features
layer = QgsVectorLayer("Point?crs=EPSG:20137&memory", "min max layer", "memory")

# Add the features to the layer
layer.dataProvider().addAttributes(joinedLayer['OUTPUT'].fields())
layer.dataProvider().addFeatures(outputFeatures)

# Add the layer to the current project
QgsProject.instance().addMapLayer(layer)

