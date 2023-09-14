class Sampler():
    def randomSample(self, compList: list, size=5) -> list:
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
