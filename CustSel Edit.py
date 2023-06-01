layer2 = QgsProject.instance().mapLayersByName('Customers_Surveyed_in_DMA_002_and_026')[0]
layer1 = QgsProject.instance().mapLayersByName('Customers_Assigned_11_Zones DMA Cutout — customers_assigned_11_zones cutout')[0]

# Check if 'Match' field already exists in both layers
if 'Match' not in [field.name() for field in layer1.fields()]:
    # If 'Match' field does not exist in layer1, add it
    layer1.startEditing()
    layer1.addAttribute(QgsField('Match', QVariant.String))
    layer1.updateFields()

if 'Match' not in [field.name() for field in layer2.fields()]:
    # If 'Match' field does not exist in layer2, add it
    layer2.startEditing()
    layer2.addAttribute(QgsField('Match', QVariant.String))
    layer2.updateFields()

# Create a list of matches for each feature in both layers
matches = ['match' if feature1['CUSTOMERKE'] == feature2['CUST_KEY'] else 'no match' for feature1, feature2 in zip(layer1.getFeatures(), layer2.getFeatures())]

# Update the 'Match' field for each feature in both layers
for i, feature in enumerate(layer1.getFeatures()):
    if matches[i] != feature['Match']:
        # If the match value has changed, update the 'Match' field
        layer1.changeAttributeValue(feature.id(), layer1.fields().indexFromName('Match'), matches[i])

for i, feature in enumerate(layer2.getFeatures()):
    if matches[i] != feature['Match']:
        # If the match value has changed, update the 'Match' field
        layer2.changeAttributeValue(feature.id(), layer2.fields().indexFromName('Match'), matches[i])

# Save changes to both layers
layer1.commitChanges()
layer2.commitChanges()