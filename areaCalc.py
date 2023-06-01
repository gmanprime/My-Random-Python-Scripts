from qgis.core import QgsDistanceArea

#get Layer of interest 
layer = iface.activeLayer()

da = QgsDistanceArea()
da.setEllipsoid('EPSG:20137')
da.setSourceCrs(layer.crs(), QgsProject.instance().transformContext())
da.setDestinationCrs(layer.crs())

# Add new field to attribute table
layer_provider = layer.dataProvider()
layer_provider.addAttributes([QgsField("area", QVariant.Double)])
layer.updateFields()

# Calculate area and update attribute table
with edit(layer):
    for feature in layer.getFeatures():
        geom = feature.geometry()
        points = geom.asPolygon()[0]
        polygon = QgsGeometry.fromPolygonXY([points])
        area = da.measurePolygon(points)
        feature["area"] = area
        layer.updateFeature(feature)
