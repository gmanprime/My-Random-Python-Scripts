from qgis.core import *

meterLayer = QgsProject.instance().mapLayersByName('CM_08112023')[0]
custlayer = QgsProject.instance().mapLayersByName('CUSTOMER_08112023')[0]

lineLayer = QgsVectorLayer('LineString', 'MyLineLayer', 'memory')

metrFeats = list(meterLayer.getFeatures())
custFeats = list(custlayer.getFeatures())

pt1 = metrFeats[0]
ppt1 = pt1.geometry().asPoint()

pt2 = custFeats[1]
ppt2 = pt2.geometry().asPoint()

lineGeom = QgsGeometry.fromPolyline(
    [
        QgsPoint(ppt1.x(), ppt1.y()),
        QgsPoint(ppt2.x(), ppt2.y()),
    ]
)

feature = QgsFeature(lineLayer.fields())
feature.setGeometry(lineGeom)

lineLayer.dataProvider().addAttributes(
    [
        QgsField("fid", QVariant.Double)
    ]
)
lineLayer.updateFields()
lineLayer.dataProvider().addFeature(feature)
lineLayer.commitChanges()
QgsProject.instance().addMapLayer(lineLayer)
