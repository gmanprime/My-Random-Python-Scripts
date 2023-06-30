from qgis.core import QgsFeature, QgsVectorLayer, QgsCoordinateReferenceSystem as QCRS
from qgis.core import QgsField, QgsGeometry, QgsProject, QgsFields, NULL
from PyQt5.QtCore import QVariant as QVar
import multiprocessing
import statistics as stats
import time
import random
import re
import collections.abc as cc
from pprint import pprint as pp


class customerPostFix():

    def __init__(self, layerName, checkFields):
        # Initializes the class object
        global projectCrs, features, layer, outputLayer
        self.checkFields = checkFields

        outputLayer = QgsVectorLayer(
            "Point?crs=EPSG:20137&memory", "minmax layer", "memory")
        layer = QgsProject.instance().mapLayersByName(layerName)[0]
        features = []

        for feature in layer.getFeatures():
            features.append(feature)

        # The CRS used in th project overall, in most cases using the Adindan:20137
        projectCrs = QCRS("EPSG:20137")

        self.target_fields_diam = [
            'Jan 2022_M_DIAMETER',
            'Feb 2022_M_DIAMETER',
            'Mar 2022_M_DIAMETER',
            'Apr 2022_M_DIAMETER',
            'May 2022_M_DIAMETER',
            'June 2022_M_DIAMETER',
            'Aug 2022_M_DIAMETER',
            'Sep 2022_M_DIAMETER',
            'Oct 2022_M_DIAMETER',
            'Nov 2022_M_DIAMETER',
            'Dec 2022_M_DIAMETER',
        ]

        self.target_fields_cons = [
            'Jan 2022_TOT_CONS',
            'Feb 2022_TOT_CONS',
            'Mar 2022_TOT_CONS',
            'Apr 2022_TOT_CONS',
            'May 2022_TOT_CONS',
            'June 2022_TOT_CONS',
            'Aug 2022_TOT_CONS',
            'Sep 2022_TOT_CONS',
            'Oct 2022_TOT_CONS',
            'Nov 2022_TOT_CONS',
            'Dec 2022_TOT_CONS',
        ]

    def _subsetCheck(self, l1, l2):
        d1 = True
        d2 = True

        # one way check for subset
        for val in l1:
            if val not in l2:
                d1 = False

        # other way check for subset
        for val in l2:
            if val not in l1:
                d2 = False

        return d1 or d2

    def featurePrint(self, feature):
        """
        This function prints the feature's field name, and attribute value on a line and wraps to new line
        to finish printing the feature's complete attribute values

        Args:
            feature (QgsFeature): Qgis feature object
        """

        keys = feature.fields().names()
        values = feature.attributes()

        for i, key in enumerate(keys):
            print(key, ': ', values[i])

    def featureValidity(self, feature):
        """
        this function takes in a feature and returns weather said feature is viable for 
        data correction and postfix operations
        """
        global layer
        target_fields_cons = self.target_fields_diam
        target_fields_diam = self.target_fields_diam
        checkFields = self.checkFields

        validity = False

        # check if inserted feature is correct type
        if (self._subsetCheck(checkFields, feature.fields().names())):
            for name in target_fields_cons:
                if (feature[name] != None):
                    validity = True

            for name in target_fields_diam:
                if (feature[name] != None):
                    validity = True
        else:
            print("This feature is not supported, use features from the 'Customer_Assigned_Billing_Data_2022_DMA_Intermitent' layer")

        return validity

    def featuresFilter(self, field, val):
        global features
        filteredList = []
        for feature in features:
            if (feature[field] == val):
                filteredList.append(feature[field])

    def fillAverage(self, feature):
        """
        takes in a feature of the customer billing type and returns the average consumption rate for the customer feature
        """

        global features
        refFields = self.target_fields_cons
        # List of non null consumption values for feature
        consRates = []
        average = 0

        # separate consumption null values from list
        for field in refFields:
            if (feature[field] != NULL):
                filteredVals = self.regNumFilter(feature[field])

                if filteredVals != []:
                    consRates.append(
                        float(
                            filteredVals[0]
                        )
                    )

        if (consRates != []):
            average = stats.mean(consRates)
            # return average

        oldGeom = feature.geometry()
        newFeature = QgsFeature()
        newFeature.setGeometry(oldGeom)
        newFields = QgsFields()

        for fieldName in feature.fields().names():
            if (fieldName != refFields[-1] and fieldName != self.target_fields_diam[-1]):
                newFields.append(
                    QgsField(
                        fieldName,
                        QVar(feature[fieldName]).type()
                    )
                )
            else:
                # add normal field
                newFields.append(
                    QgsField(
                        fieldName,
                        QVar(feature[fieldName]).type()
                    )
                )

                # add averages field
                newFields.append(
                    QgsField(
                        'AVG_CONS',
                        QVar.Double
                    )
                )

        newFeature.setFields(newFields)

        # add the values to the fields
        for fieldName in newFeature.fields().names():
            # print(fieldName, ': ',
            #       average if fieldName not in feature.fields().names() else feature[fieldName])

            if (fieldName == 'fid'):
                pass
            elif (fieldName == 'AVG_CONS'):
                newFeature.setAttribute(fieldName, QVar(average).value())
                # newFeature[fieldName] = QVar(average).value()
            else:
                newFeature.setAttribute(
                    fieldName, QVar(feature[fieldName]).value())
                # newFeature[fieldName] = QVar(feature[fieldName]).value()

        return newFeature

    def cleanList(self, FullList, criteria):
        """
        This function takes a list of values returns a list with values that meet the criteria added as a lambda functions to

        Args:
            FullList (list): LIst of items that need to be filtered out
            criteria (lambda function): function that returns a Truth value for If condition

        Returns:
            List: List of filtered values based on the lambda function
        """

        cleanList = []
        for value in FullList:
            if type(criteria(value)) is not bool:
                print(
                    "The conditional lambda function is not a bool conditional function")
                cleanList = []
                break

            if criteria(value):
                cleanList.append(value)
        return cleanList

    def copyPaste(self, feature):
        """
        this method checks weather a value for a given set of attributes is the same in all the attributes and copies it
        to fields with None or null values

        Args:
            feature (QgsFeature): QGIS layer feature under processing
        """
        refFields = self.target_fields_diam

        # consumption ID pattern
        rePattern = r"\w+ \w+\_DIAMETER$"
        flags = re.IGNORECASE | re.MULTILINE | re.DOTALL

        # will contains all relevant values
        values = []

        # check weather a feature is valid
        if (self.featureValidity(feature)):
            # extracts relevant values from the feature
            for key in refFields:
                # check if field is a Diameter field using regex
                if re.match(rePattern, key, flags):
                    # append value to values array if it is a diameter field
                    values.append(feature[key])
        else:
            values.append(False)

        # NOTE: I've got the diameter values extracted from the diameter fields
        # NOTE: now i have to check weather all the values that are not NONE have the same value
        # NOTE: then i have to return the value that matches, if it doesnt match then return a list with FALSE

        cleanList = self.cleanList(
            values, lambda val: type(val) is not QVar
        )

        diam = stats.mode(cleanList)

        oldGeom = feature.geometry()
        newFeature = QgsFeature()
        newFeature.setGeometry(oldGeom)
        newFields = QgsFields()

        # WARNING: Need to use filtered checkFields for only diameter pipe values

        for fieldName in feature.fields().names():
            if (fieldName in refFields):
                newFields.append(
                    QgsField(
                        fieldName,
                        # feature.fields().field(fieldName).type(),
                        QVar(float(diam)).type()
                    )
                )

            elif (fieldName == 'fid'):
                pass
            else:
                newFields.append(
                    QgsField(
                        fieldName,
                        QVar(feature[fieldName]).type()
                    )
                )
        newFeature.setFields(newFields)

        for fieldName in newFeature.fields().names():
            if (fieldName in refFields):
                newFeature.setAttribute(fieldName, QVar(float(diam)).value())
                # newFeature[fieldName] = QVar(float(diam)).value()
            elif (fieldName == 'fid'):
                pass
            else:
                newFeature.setAttribute(
                    fieldName, QVar(feature[fieldName]).value())
                # newFeature[fieldName] = QVar(feature[fieldName]).value()
        self.newFeature = newFeature
        return newFeature

    def regNumFilter(self, text):
        pattern = r'^[0-9]+\s*$'
        matches = []

        if type(text == 'string'):
            matches = re.findall(pattern, text, re.MULTILINE)
        else:
            print('incompatible type of input')
        return matches

    def randomSample(self, compList, size=5):
        """
        Extracts a random sample from a list of objects

        Args:
            size (Int): the size of the list of objects to extract,
            compList (list): the list of objects to extract from
        returns:
            sampleList (list): a random sample list
        """

        # length of the list of possible range
        max_len = len(compList) - 1

        # pick a random index number from the length of the list
        rangeStart = random.randrange(0, max_len)

        # add the size to the starting index to get the last index
        rangeEnd = rangeStart + size

        return compList[rangeStart:rangeEnd]

    def addToLayer(self):
        global layer, outputLayer

        # newFeatures = []

        for feature in features:
            featProcessing = self.copyPaste(feature)
            featProcessing = self.fillAverage(featProcessing)
            # newFeatures.append(featProcessing)
            outputLayer.dataProvider().addFeature(featProcessing)

        outputLayer.dataProvider().addAttributes(
            layer.fields()
        )

        outputLayer.updateFields()

        return outputLayer

    def mapExport(self):
        """
        will export the output layer to the QGIS map
        """
        global outputLayer

        if (outputLayer):
            # Add the layer to the current project
            QgsProject.instance().addMapLayer(outputLayer)


def killRun(process, kill_time):
    p = multiprocessing.Process(target=process)
    p.start()
    time.sleep(kill_time)
    p.terminate()


def main():
    global fixr, checkFields, features
    checkFields = [
        # 'fid',
        # 'CUSTOMERKE',
        # 'INST_KEY',
        # 'CONTRACT_NUMBER',
        # 'CHARGE_GROUP',
        # 'ROUTE_KEY',
        # 'WALK_ORDER',
        # 'LATTITUDE',
        # 'LONGITUDE',
        # 'ALTITUDE',
        # 'CUST_NAME',
        # 'CHARGE_GRO',
        # 'TOTAL_CONS',
        # 'METER_DIAM',
        # 'WEREDA_AAWSA_DB',
        # 'HOUSE_NUMB',
        # 'S_CITY_AAWSA_DB',
        # 'OLD_WEREDA',
        # 'OLD_KEBELE',
        # 'Sub_city_2022',
        # 'Woreda_2022',
        # 'Date Added',
        # 'Date modified',
        # 'Editor',
        # 'MeterNo',
        # 'customerAd',
        # 'customerBr',
        # 'routeId',
        # 'Zone',
        # 'DMA',
        # 'Date Created',
        # 'D_Accuracy',
        'Jan 2022_TOT_CONS',
        'Jan 2022_M_DIAMETER',
        'Feb 2022_TOT_CONS',
        'Feb 2022_M_DIAMETER',
        'Mar 2022_TOT_CONS',
        'Mar 2022_M_DIAMETER',
        'Apr 2022_TOT_CONS',
        'Apr 2022_M_DIAMETER',
        'May 2022_TOT_CONS',
        'May 2022_M_DIAMETER',
        'June 2022_TOT_CONS',
        'June 2022_M_DIAMETER',
        'Aug 2022_TOT_CONS',
        'Aug 2022_M_DIAMETER',
        'Sep 2022_TOT_CONS',
        'Sep 2022_M_DIAMETER',
        'Oct 2022_TOT_CONS',
        'Oct 2022_M_DIAMETER',
        'Nov 2022_TOT_CONS',
        'Nov 2022_M_DIAMETER',
        'Dec 2022_TOT_CONS',
        'Dec 2022_M_DIAMETER',
        # 'Shift_Code',
        # 'Name',
        # 'Description',
        # 'Water Distribution',
        # 'AAWSA Delineation'
    ]

    fixr = customerPostFix(
        'Customer_Assigned_Billing_Data_2022_DMA_Intermitent', checkFields)

    fixr.addToLayer()
    fixr.mapExport()


main()
