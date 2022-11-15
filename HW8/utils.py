# ----------------------------------------------------------------------
# Name:     utils
# Purpose:  Useful functions for homework 8
#
# Author:   Rula Khayrallah
#
# ----------------------------------------------------------------------

def manhattan_distance(point1, point2):
    """
    Compute the Manhattan distance between two points.
    :param point1 (tuple) representing the coordinates of a point in a plane
    :param point2 (tuple) representing the coordinates of a point in a plane
    :return: (integer)  The Manhattan distance between the two points
    """
    x1, y1 = point1
    x2, y2 = point2
    distance = abs(x1 - x2) + abs(y1 - y2)
    return distance


def closest_point(point1, other_points):
    """
    Find the coordinates of the closest point to point1
    :param point1 (tuple) representing the coordinates of a point =
    :param other_points(list) representing several points in a plane
    :return: (tuple) the coordinates of the closest point to point1

    """
    if not other_points:
        return None
    closest = min(other_points, key=lambda p: manhattan_distance(point1, p))
    return closest
