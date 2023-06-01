import PyQt5

#determine truthvalues from a list of truth conditions
def isAndTrue(condition = [False]):
    TruthState = True;
    for cond in condition:
        TruthState = TruthState and cond
    return TruthState

def lenByCatagory(layerName, catagoryGroup, category_name, field_name):
    
    #get list of all layers from project and extract layers with specific name
    layers =QgsProject.instance().mapLayersByName(layerName) 
    
    #extract first available layer with designated name
    layer = layers[0]
    
    # toatal length of pipe belonging to a catagory
    totalZonesLength = 0
    length = 0
    
    #extract all features from layer
    allFeatures = list(layer.getFeatures())
    
    #compute length of feature in all zones
    for feature in allFeatures:
        condition = [
        isinstance(feature[field_name], float),
        feature['Zone_Name'] != NULL,
        feature['Zone_Name'] != 'ZONE 12',
        feature['NOM_DIAM'] >= 50 
        ]
        
        if isAndTrue(condition):
            totalZonesLength += feature[field_name]

    #loop through float type feature in a catagory of items
    for feature in allFeatures:
        # Check if feature belongs to category and add the lenth of it is
        
        #filter conditions
        condition = [
        isinstance(feature[field_name], float),
        feature[catagoryGroup] == category_name,
        feature['Zone_Name'] != NULL,
        feature['Zone_Name'] != 'ZONE 12',
        feature['NOM_DIAM'] >= 50 
        ]
        
        if isAndTrue(condition):
                length += feature[field_name]
                
        elif isinstance(feature[field_name], PyQt5.QtCore.QVariant):
            #PyQt5.QtCore.QVariant types represent the null value in the table
            if  feature[catagoryGroup] == category_name:
                #do nothing
                length = length
                
    print(round(totalZonesLength,2))
    return round(length, 2)
    
    
print(lenByCatagory('Pipes_Selected_for_Report_April_2023 (2) — Pipes_50mm_and_above_in_11_Zones', 'Report_Remark', 'AAWSA Original', 'Length_km'))
print(lenByCatagory('Pipes_Selected_for_Report_April_2023 (2) — Pipes_50mm_and_above_in_11_Zones', 'Report_Remark', 'New (Miya)', 'Length_km'))
print(lenByCatagory('Pipes_Selected_for_Report_April_2023 (2) — Pipes_50mm_and_above_in_11_Zones', 'Report_Remark', 'Updated (Miya)', 'Length_km'))
print(lenByCatagory('Pipes_Selected_for_Report_April_2023 (2) — Pipes_50mm_and_above_in_11_Zones', 'Report_Remark', 'Joint Update Attribute', 'Length_km'))
print(lenByCatagory('Pipes_Selected_for_Report_April_2023 (2) — Pipes_50mm_and_above_in_11_Zones', 'Report_Remark', 'Joint Update New', 'Length_km'))