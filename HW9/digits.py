# ----------------------------------------------------------------------
# Name:        digits
# Purpose:     Homework 9
#
# Author:      Rula Khayrallah
#
# ----------------------------------------------------------------------
"""
Read the digit image and label files and build a list of Example objects
"""
import numpy as np
IMAGE_SIZE = 28
NUM_FEATURES = IMAGE_SIZE ** 2 + 1
from example import Example


def read(images, labels):
    """
    Read the digits image and label files and build the
    example objects with the feature vectors.
    :param images: Name of the text file containing the images
    :param labels: Name of the text file containing the labels
    :return: A list of Example objects
    """
    data = []
    with open(labels, 'r', encoding='utf-8') as label_file:
        for each_line in label_file:
            example = Example(int(each_line.strip()))
            data.append(example)

    image_row = 0
    count = 0
    with open(images, 'r', encoding='utf-8') as image_file:
        for each_line in image_file:
            if image_row == 0:
                feature_vector = np.zeros(NUM_FEATURES, int)
                feature_vector[0] = 1 # bias
                feature = 1
            for each_char in each_line[0:IMAGE_SIZE]:
                feature_vector[feature] = 0 if each_char == ' ' else 1
                feature += 1
            image_row = (image_row + 1) % IMAGE_SIZE
            if image_row == 0:
                data[count].fvector = feature_vector
                count += 1
    data[-1].fvector = feature_vector
    return data

