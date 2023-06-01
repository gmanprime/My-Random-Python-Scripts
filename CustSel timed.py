import random
import time
import numpy as np
import matplotlib.pyplot as plt

l2 = QgsProject.instance().mapLayersByName('Customers_Surveyed_in_DMA_002_and_026')[0]
l1 = QgsProject.instance().mapLayersByName('Customers_Assigned_11_Zones DMA Cutout — customers_assigned_11_zones cutout')[0]

# Add new fields to both layers
l1.startEditing()
l1.addAttribute(QgsField('Match', QVariant.String))
l1.updateFields()

l2.startEditing()
l2.addAttribute(QgsField('Match', QVariant.String))
l2.updateFields()

#The avge time measurements for testing
avgTimes = []

#the size of the list for testing. will be changed to actuall customer numbers later on
lSize = 10

#how many times to run the test
reps = 5
#
#def getFeatures(centFeat, radius):
#    #function to get features from layers bound withing a specific radius
#    index = QgsSpatialIndex(l1.getFeatures())
#    nearest = index.nearestNeighbor(feature.geometry().asPoint(), radius)
#    features = [f for f in layer.getFeatures() if f.id() in nearest]
#    return features
#
#testing function, will test the code in time
def test():
    start_time = time.time_ns()//1_000_000
    count = 0
    
    for feature1 in l1.getFeatures():
        if(count <= lSize):
            for feature2 in getFeatures(feature1, 10):
                if feature1['CUSTOMERKE'] == feature2['CUST_KEY']:
                    # Set the Match field to 'match' if the fields match
                    l1.changeAttributeValue(feature1.id(), l1.fields().indexFromName('Match'), 'match')
                    l2.changeAttributeValue(feature2.id(), l2.fields().indexFromName('Match'), 'match')
                    
                else:
                    # Set the Match field to 'no match' if the fields don't match
                    l1.changeAttributeValue(feature1.id(), l1.fields().indexFromName('Match'), 'no match')
                    l2.changeAttributeValue(feature2.id(), l2.fields().indexFromName('Match'), 'no match')
        else:
            break
        count+=1
    
    end_time = time.time_ns()//1_000_000

    execution_time = end_time - start_time
    print('Execution time in seconds:', execution_time/1000)
    avgTimes.append(execution_time)


for i in range(reps):
    test()

print("The average time is:", np.mean(avgTimes) /
      1000, "s for ", lSize, " list Size")

x = np.arange(0, reps, 1)

rangeArr = []

for i in range(reps):
    rangeArr.append(np.mean(avgTimes))


plt.plot(x, avgTimes)
plt.plot(x, rangeArr)
plt.show()
