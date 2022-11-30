# ----------------------------------------------------------------------
# Name:        example
# Purpose:     Homework 9
#
# Author:      Rula Khayrallah
# ----------------------------------------------------------------------
"""
Class definition for example data structure to be used by the perceptron
"""

class Example:
    """
    Represent an example (training, validation or test)
    Arguments:
        label: (may be integer or string) training label
        fvector: (NumPy array)) feature vector - defaults to None

    Attributes:
        label: (may be integer or string) training label
        fvector: (NumPy array)) feature vector
    """
    def __init__(self, label, fvector=None):
        self.label = label
        self.fvector = fvector

    @property
    def number_of_features(self):
        """
        The number of features for the given example
        :return: integer
        """
        return len(self.fvector)


    def distance(self, other):
        """
        Compute the Euclidean distance between the two feature
        vectors representing the given examples.
        :param other: (Example object)
        :return: float
        """
        diff = (self.fvector - other.fvector) ** 2
        return diff.sum() ** 0.5


