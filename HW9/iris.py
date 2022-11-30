# ----------------------------------------------------------------------
# Name:        iris
# Purpose:     Homework 9
#
# Author:      Rula Khayrallah
# ----------------------------------------------------------------------
"""
This module preprocesses the Iris CSV dataset
"""
from example import Example
import numpy as np


def read(filename):
    """
    Read the Iris csv file and construct the Example objects.
    The file is assumed to contain 5 columns:
    sepal length, sepal width, petal length, petal width and training label.
    The first 4 columns will be used as features in the feature vector
    constructed.

    :param filename: Name of the csv file containing iris data
    :return: A list of Example objects
    """
    data = []
    labels = []
    with open(filename, 'r', encoding='utf-8') as label_file:
        for each_line in label_file:
            example_data = each_line.strip().split(',')
            num_features = len(example_data)
            feature_vector = np.zeros(num_features, float)
            feature_vector[0] = 1 # bias
            for count in range(num_features - 1):
                feature = float(example_data[count])
                feature_vector[count + 1] = feature
            label = example_data[num_features - 1]
            example = Example(label, feature_vector)
            data.append(example)
    return data