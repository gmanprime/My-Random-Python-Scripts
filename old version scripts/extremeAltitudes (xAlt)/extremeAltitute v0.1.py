import processing
from qgis.core import QgsProject, QgsProcessing

# get the active polygon layer
dmaBoundary = QgsProject.instance().mapLayersByName('DMA_Boundary_V3')[0]

# get the raster layer
rasterLayer = QgsProject.instance().mapLayersByName('Addis_Ababa_Elevation')[0]

for feature in dmaBoundary.getFeatures():
    processing.run("qgis:rastervaluestopoints", {
        'GRIDS': rasterLayer,
        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    })
    
    processing.run("qgis:joinattributesbylocation", {
        'INPUT': feature,
        'JOIN': QgsProcessing.TEMPORARY_OUTPUT,
        'PREDICATE': [1],
        'JOIN_FIELDS': ['elevation'],
        'METHOD': 0,
        'DISCARD_NONMATCHING': False,
        'PREFIX': '',
        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    })
    processing.run("qgis:statisticsbycategories", {
        'INPUT': QgsProcessing.TEMPORARY_OUTPUT,
        'VALUES_FIELD_NAME': ['elevation'],
        'CATEGORIES_FIELD_NAME': [],
        'OPERATIONS': [1, 2],
        'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
    })
