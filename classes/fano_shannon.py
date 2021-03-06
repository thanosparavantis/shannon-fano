"""
    Theoria pliroforion kai kodikon
    Ioulios 2018

    == Developed using Python 3.6.5 by ==
    == p16036 - Ioannidis Panagiotis   ==
    == p16097 - Nikas Dionisis         ==
    == p16112 - Paravantis Athanasios  ==
"""
import math

class FanoShannon:
    def __init__(self):
        self.result = {}

    def compress(self, sequence, code=""):
        group_a = {}
        group_b = {}

        if len(sequence) == 1:
            self.result[sequence.popitem()[0]] = code
            return 0

        # Sum the values of the dict
        sum_values = sum(sequence.values())

        # Find the half of the sum
        half = sum_values / 2

        sum_half = 0
        for i in sequence:
            # Sum the values of the dict until the sum_half will be
            # grater than the half and append it in dict group_a
            if sum_half < half:
                sum_half += sequence[i]
                group_a[i] = sequence[i]
            else:
                # else append it in dict group_b
                group_b[i] = sequence[i]

        # Execute recursively the method for the group_a and group_b
        self.compress(group_a, code + "0")
        self.compress(group_b, code + "1")

    def get_mappings(self):
        return self.result

    def get_entropy(self, probabilities):
        probability_list = sorted(list(probabilities))

        entropy = 0
        for i in probability_list:
            entropy += i*math.log(1/i, 2)
        return entropy