from pprint import pprint as pp
import fiona  # ? not sure what this does ?
import geopandas as gpd  # geo analysis toolbox based on pandas data analysis toolbox
import os  # used for accessing Operating system functionality, in this case, the path computation tools
import argparse  # can be used to get arguments trailing the python call when running code

# test file path to GeoPackage
tempPath = os.path.join(os.path.expanduser(
    "~"), "Documents", "AnalysisPackages", "customerCompare.gpkg")


class GeoCompare():

    # object initializer
    def __init__(self, geoPackagePath=tempPath):
        self.geoPath = geoPackagePath  # set the path to the global variable space as geoPath
        # extract the layers from the geopackage file
        self.layers = fiona.listlayers(geoPackagePath)
        self.geoData = {}  # create a global dictionary file to contain all the geodata
        self.customerKeys = {}  # list of customer keys divided by layer

    def idMatch(self):
        # This function compares the specified id value from an attribute
        for layer in self.layers:
            # read the data from the geopackage file, and specifically a layer from the fiona module
            self.geoData[layer] = gpd.read_file(
                self.geoPath, layer=layer).to_dict(orient='records')

            # set the layer array list of customers to empty array
            self.customerKeys[layer] = {}

            # add the customers to the layers array list
            for recordDict in self.geoData[layer]:
                if ("CUSTOMERKE" not in recordDict and recordDict['CUST_KEY'] != None):
                    # add the customer key to the dict as a key with value of True
                    self.customerKeys[layer][recordDict['CUST_KEY']] = True
                elif ("CUSTOMERKE" in recordDict):
                    # add the customer key to the dict as a key with value of True
                    self.customerKeys[layer][recordDict['CUSTOMERKE']] = True

        # get the list of customer keys from first dictionary
        for key, value in self.customerKeys[self.layers[0]].items():
            if key in self.customerKeys[self.layers[1]].keys():
                Match = value == self.customerKeys[self.layers[1]][key]
                if Match:
                    self.customerKeys[self.layers[0]][key] = False
                    self.customerKeys[self.layers[1]]

    @classmethod  # lets us use the method in the if __name__ == '__main__': computation below
    def main(cls, filePath):
        geoObj = cls(filePath)
        geoObj.idMatch()


if __name__ == '__main__':
    GeoCompare.main(os.path.join(os.path.expanduser(
        "~"), "Documents", "AnalysisPackages", "customerCompare.gpkg")
    )
