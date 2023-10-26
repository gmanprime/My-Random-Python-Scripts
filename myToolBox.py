""" 
This python file can be used to abstract away recusivley used tools across multiple scripts
"""
import random
import re
import sys
import argparse
from pprint import pprint as pp


class toolBox():
    def __init__(self):
        pass

    def randomSample(self, fullList, size=8):
        """
        Extracts a random sample (by default 8) from a list of objects

        Args:
            size (Int): the size of the list of objects to extract,
            compList (list): the list of objects to extract from
        returns:
            sampleList (list): a random sample list
        """

        # length of the list of possible range
        max_len = len(fullList) - 1

        # pick a random index number from the length of the list
        rangeStart = random.randrange(0, max_len)

        # add the size to the starting index to get the last index
        rangeEnd = rangeStart + size

        return fullList[rangeStart:rangeEnd]

    def regFilter(self, stringList, regPattern):
        """
        This method takes in a list of strings and returns a list of strings that match the 
        regex pattern specified in the parameters.add()

        Args:
            stringList ([string, string,...]): list of strings that is to be filtered
            regPattern (r"pattern"): regex pattern in python syntax 

        Returns:
            [string, string, ...]: list of filtered strings that fully or partially match the regex pattern
        """

        matches = []
        for text in stringList:
            if type(text == str):
                matchVal = re.findall(regPattern, text, re.MULTILINE)
                if (len(matchVal) == 1):  # check for single match value
                    matches.append(matchVal[0])
                elif len(matchVal) != 0:
                    matches.append(matchVal)

        return matches


def _argManager():
    # globalize the arguments for access across the script
    global args
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--testing",
        "-t",
        help="testing mode on or off.",
        default="n"
    )

    args = parser.parse_args()

    return args


def _test():
    testStringList = [
        "12345678901234567890",
        "98765432109876543210",
        "4abcdefghijklmnopqrstuvwxyz",
        "John Doe",
        "William Brown",
        "Jane Doe",
        "Michael Smith",
        "3!@#$%^&*()_+-=[]:;'<>,./?",
        "5ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "212345678901234567890",
        "765432109876543210",
        "12345678901234567892",
        "6abcdefghijklmnopqrstuvw",
        "James Smith",
        "Emily Jones",
        "Thomas Doe",
        "Sarah Brown",
        "9&*()_+-=[]:;'<>,./?@#",
        "8XYZABCDEFGHIJKLMNOPQ",
        "41234567890123456789",
        "654321098765432100",
        "12345678901234567893",
        "7abcdefghijklmnopqrstuvwxyz",
        "Jessica Smith",
        "Benjamin Jones",
        "Victoria Doe",
        "Matthew Brown",
        "0&*()_+-=[]:;'<>,./?@#$",
        "9WXYZABCDEFGHIJKLMNOPQR",
        "51234567890123456789"
    ]
    toolbox = toolBox()  # create new toolbox object
    fList = toolbox.regFilter(testStringList, r"^\d+")
    pp(fList)


def _main():
    global args
    if args.testing == 'y':
        _test()


if __name__ == "__main__":
    _argManager()  # runs the argument manger to get and globalize the arguments object
    _main()        # runs the default main() startup function
