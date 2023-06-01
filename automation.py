fn = 'c:/Users/Yonatan/Documents/QGIS/QGIS Data Sources/AAWSN/shape files/Point.shp'

def getData(shpFile,attrib):
    # Get data from attrib table
    layer = QgsVectorLayer(shpFile,"",'ogr')
    
    fc = layer.featureCount()
    
    for i in range(0,fc):
        currentFeat = layer.getFeature(i)
        print(currentFeat[attrib])
    return None
        
getData(fn, "layer")clear
