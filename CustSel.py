import time
layer2 = QgsProject.instance().mapLayersByName('Customers_Surveyed_in_DMA_002_and_026')[0]
layer1 = QgsProject.instance().mapLayersByName('Customers_Assigned_11_Zones DMA Cutout — customers_assigned_11_zones cutout')[0]

# Add new fields to both layers
layer1.startEditing()
layer1.addAttribute(QgsField('Match', QVariant.String))
layer1.updateFields()

layer2.startEditing()
layer2.addAttribute(QgsField('Match', QVariant.String))
layer2.updateFields()
    
#***********************************
#WORKING POINT: Verifued Everything works untill this point

start_time = time.time_ns()//1_000_000
x = 0

for feature1 in layer1.getFeatures():
    for feature2 in layer2.getFeatures():
        if feature1['CUSTOMERKE'] == feature2['CUST_KEY'] and x <= 10:
            # Set the Match field to 'match' if the fields match
            layer1.changeAttributeValue(feature1.id(), layer1.fields().indexFromName('Match'), 'match')
            layer2.changeAttributeValue(feature2.id(), layer2.fields().indexFromName('Match'), 'match')
            
        elif x > 10:
            # Set the Match field to 'no match' if the fields don't match
            layer1.changeAttributeValue(feature1.id(), layer1.fields().indexFromName('Match'), 'no match')
            layer2.changeAttributeValue(feature2.id(), layer2.fields().indexFromName('Match'), 'no match')
            
    x+=1
            
end_time = time.time_ns()//1_000_000

execution_time = end_time - start_time
print('Execution time in millySeconds:', execution_time)
            
layer1.commitChanges()
layer2.commitChanges()