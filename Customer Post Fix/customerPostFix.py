import qgis.core as qgs
import multiprocessing
import time
import re
import collections.abc as cc
from pprint import pprint as pp


QgsVectorLayer = qgs.QgsVectorLayer
QCRS = qgs.QgsCoordinateReferenceSystem
QgsField = qgs.QgsField
QgsGeometry = qgs.QgsGeometry
QgsProject = qgs.QgsProject


class customerPostFix():

    def __init__(self, layerName, checkFields):
        # Initializes the class object
        global projectCrs, features, layer
        self.checkFields = checkFields

        self.outputLayer = QgsVectorLayer("Point", "MyLayer", "memory")
        layer = QgsProject.instance().mapLayersByName(layerName)[0]
        features = []

        for feature in layer.getFeatures():
            features.append(feature)

        # The CRS used in th project overall, in most cases using the Adindan:20137
        projectCrs = QCRS("EPSG:20137")

        self.target_fields_cons = [

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

        self.target_fields_diam = [
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
        target_fields_cons = self.target_fields_cons
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

    def copyPaste(self, feature):
        """
        this method checks weather a value for a given set of attributes is the same in all the attributes and copies it
        to fields with None or null values

        Args:
            feature (QgsFeature): QGIS layer feature under processing
        """
        checkFields = self.checkFields

        # consumption ID pattern
        rePattern = r"\w+ \w+\_DIAMETER$"
        flags = re.IGNORECASE | re.MULTILINE | re.DOTALL

        # will contains all relevant values
        values = []

        # check weather a feature is valid
        if (self.featureValidity(feature)):
            # extracts relevant values from the feature
            for key in checkFields:
                # check if field is a Diameter field using regex
                if re.match(rePattern, key, flags):
                    # append value to values array if it is a diameter field
                    values.append(feature[key])
        else:
            values.append(False)

        # NOTE: ive got the diameter values extracted from the diameter fields
        # NOTE: now i have to check weather all the values that are not NONE have the same value
        # NOTE: then i have to return the value that matches, if it doesnt match then return a list with FALSE

        pp(values)

    def postulate(self, attributes):
        """
        this function generates new data for any input feature based on the features current data and on weather
        its postfix capable
        """
        pass

    def sumConsumption(self, feature):
        pass

    def fillIn(self):
        """
        This tool will update the new Temp QGIS layer using the list of items generated 
        by the classify tool
        """

    def mapExport(self):
        """
        will export the output layer to the QGIS map
        """
        outputLayer = self.outputLayer

        if (outputLayer):
            # Add the layer to the current project
            QgsProject.instance().addMapLayer(outputLayer)


def killRun(process, kill_time):
    p = multiprocessing.Process(target=process)
    p.start()
    time.sleep(kill_time)
    p.terminate()


def main():
    global fixr, checkFields
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


main()
