from qgis.core import QgsDistanceArea, QgsFeature, QgsFeatureRequest, QgsField, QgsFields, QgsGeometry, QgsPoint, QgsProject, QgsVectorLayer
from qgis.PyQt.QtCore import QVariant

def group_points_by_proximity_and_field(layer, proximity, field):
    # Create a new field to store the group number
    group_field = QgsField('Group', QVariant.Int)
    layer.dataProvider().addAttributes([group_field])
    layer.updateFields()

    # Create a dictionary to store the group number for each feature
    group_dict = {}

    # Create a list to store the features that have not been assigned to a group
    ungrouped_features = []

    # Create a distance area object to calculate distances
    distance_area = QgsDistanceArea()
    distance_area.setEllipsoid('WGS84')

    # Loop through each feature in the layer
    for feature in layer.getFeatures():
        # Get the point geometry and the value of the field
        point = feature.geometry().asPoint()
        value = feature[field]

        # If the value is not in the group dictionary, create a new group
        if value not in group_dict:
            group_dict[value] = len(group_dict) + 1

        # Loop through each feature again to find nearby features
        nearby_features = []
        for other_feature in layer.getFeatures():
            # Skip the current feature
            if other_feature.id() == feature.id():
                continue

            # Get the other point geometry and calculate the distance
            other_point = other_feature.geometry().asPoint()
            distance = distance_area.measureLine(QgsPoint(point), QgsPoint(other_point))

            # If the distance is less than the proximity, add the feature to the nearby features list
            if distance < proximity:
                nearby_features.append(other_feature)

        # If there are no nearby features, add the feature to the ungrouped features list
        if not nearby_features:
            ungrouped_features.append(feature)
        else:
            # Get the group number for the feature
            group_number = group_dict[value]

            # Assign the group number to the feature
            feature[group_field.name()] = group_number
            layer.updateFeature(feature)

            # Assign the group number to the nearby features
            for nearby_feature in nearby_features:
                nearby_feature[group_field.name()] = group_number
                layer.updateFeature(nearby_feature)

    # Assign the remaining features to a group
    for feature in ungrouped_features:
        # Get the point geometry and the value of the field
        point = feature.geometry().asPoint()
        value = feature[field]

        # Get the group number for the feature
        group_number = group_dict[value]

        # Assign the group number to the feature
        feature[group_field.name()] = group_number
        layer.updateFeature(feature)

    # Return the layer
    return layer
