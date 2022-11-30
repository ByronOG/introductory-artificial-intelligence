# ----------------------------------------------------------------------
# Name:     sudoku
# Purpose:  Homework5
#
# Author: Byron O'Gorman
#
# ----------------------------------------------------------------------
"""
Sudoku puzzle solver implementation

q1:  Basic Backtracking Search
q2:  Backtracking Search with AC-3
q3:  Backtracking Search with MRV Ordering and AC-3
"""
from itertools import product

import csp

# size of puzzle
X = 9
Y = 9


# Enter your helper functions
def build_domain(puzzle):
    """
    non assigned cells are assigned all possible values (0-9) as their domain
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: domain: Dictionary of the variables and their domains
    """
    domain = {}
    for i in range(0, 9):
        for j in range(0, 9):
            tup = (i, j)
            if tup in puzzle:  # if in puzzle, add it to the domain
                value = puzzle[tup]
                domain[tup] = {value}
            else:  # else add all possible values
                domain[tup] = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    print("Domains:")
    for key in domain:
        print(key, domain[key])
    return domain


def build_neighbors(puzzle):
    """
    Find the neighboring cells(cells in the same row, column or square) of all individual cells
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: Dictionary: Dictionary of all cells and their neighbors
    """
    neighbors_dict = {}
    for i in range(0, 9):
        for j in range(0, 9):
            cell = (i, j)
            neighbors_set = gsn2(cell)
            for x in range(0, 9):  # add all cells in its row and column
                tmp_tup1 = (i, (j + x) % 9)
                tmp_tup2 = ((i + x) % 9, j)
                neighbors_set.add(tmp_tup1)
                neighbors_set.add(tmp_tup2)
            neighbors_set.remove(cell)
            neighbors_dict[cell] = neighbors_set
    print("\n\nNeighbors:")
    for key in neighbors_dict:
        print(key, neighbors_dict[key])
    return neighbors_dict


def gsn2(cell):
    """
    use integer division to find the left corner neighbor of the cell
    add all neighbors using simple arithmetic
    :param cell: square in puzzle
    :return: set of neighbors
    """
    x, y = cell
    min_x = (x // 3) * 3
    min_y = (y // 3) * 3
    neighbors = set()
    for i in range(0, 3):
        for j in range(0, 3):
            if i != x and j != y:
                neighbors.add((min_x + i, min_y + j))
    return neighbors


def get_square_neighbors(cell):
    """
    Helper function to find the neighboring cells in a cell's square
    :param cell (tuple): a cell in the problem
    :return: set of neighboring cells
    """
    square_neighbors = set()
    x, y = cell
    if x % 3 == 0:  # if cell is row index 0,3,6
        if y % 3 == 0:  # if cell is col index 0,3,6
            square_neighbors.add((x + 1, y))
            square_neighbors.add((x + 2, y))
            square_neighbors.add((x, y + 1))
            square_neighbors.add((x, y + 2))
            square_neighbors.add((x + 1, y + 1))
            square_neighbors.add((x + 1, y + 2))
            square_neighbors.add((x + 2, y + 1))
            square_neighbors.add((x + 2, y + 2))
        elif y % 3 == 1:  # if cell is col index 1,4,7
            square_neighbors.add((x + 1, y - 1))
            square_neighbors.add((x + 2, y - 1))
            square_neighbors.add((x, y - 1))
            square_neighbors.add((x, y + 1))
            square_neighbors.add((x + 1, y))
            square_neighbors.add((x + 1, y + 1))
            square_neighbors.add((x + 2, y))
            square_neighbors.add((x + 2, y + 1))
        else:  # if cell is col index 2,5,8
            square_neighbors.add((x + 1, y - 2))
            square_neighbors.add((x + 2, y - 2))
            square_neighbors.add((x, y - 2))
            square_neighbors.add((x, y - 1))
            square_neighbors.add((x + 1, y - 1))
            square_neighbors.add((x + 1, y))
            square_neighbors.add((x + 2, y - 1))
            square_neighbors.add((x + 2, y))
    elif x % 3 == 1:  # if cell is row index 1,4,7
        if y % 3 == 0:
            square_neighbors.add((x - 1, y))
            square_neighbors.add((x + 1, y))
            square_neighbors.add((x, y + 1))
            square_neighbors.add((x, y + 2))
            square_neighbors.add((x - 1, y + 1))
            square_neighbors.add((x - 1, y + 2))
            square_neighbors.add((x + 1, y + 1))
            square_neighbors.add((x + 1, y + 2))
        elif y % 3 == 1:
            square_neighbors.add((x - 1, y - 1))
            square_neighbors.add((x - 1, y))
            square_neighbors.add((x - 1, y + 1))
            square_neighbors.add((x, y - 1))
            square_neighbors.add((x, y + 1))
            square_neighbors.add((x + 1, y - 1))
            square_neighbors.add((x + 1, y))
            square_neighbors.add((x + 1, y + 1))
        else:
            square_neighbors.add((x - 1, y - 1))
            square_neighbors.add((x - 1, y - 2))
            square_neighbors.add((x - 1, y))
            square_neighbors.add((x, y - 1))
            square_neighbors.add((x, y - 2))
            square_neighbors.add((x + 1, y - 1))
            square_neighbors.add((x + 1, y - 2))
            square_neighbors.add((x + 1, y))
    else:  # else cell is row index 2,5,8
        if y % 3 == 0:
            square_neighbors.add((x - 2, y))
            square_neighbors.add((x - 2, y + 1))
            square_neighbors.add((x - 2, y + 2))
            square_neighbors.add((x - 1, y))
            square_neighbors.add((x - 1, y + 1))
            square_neighbors.add((x - 1, y + 2))
            square_neighbors.add((x, y + 1))
            square_neighbors.add((x, y + 2))
        elif y % 3 == 1:
            square_neighbors.add((x - 2, y - 1))
            square_neighbors.add((x - 2, y + 1))
            square_neighbors.add((x - 2, y))
            square_neighbors.add((x - 1, y - 1))
            square_neighbors.add((x - 1, y + 1))
            square_neighbors.add((x - 1, y))
            square_neighbors.add((x, y - 1))
            square_neighbors.add((x, y + 1))
        else:
            square_neighbors.add((x - 2, y - 2))
            square_neighbors.add((x - 2, y - 1))
            square_neighbors.add((x - 2, y))
            square_neighbors.add((x - 1, y - 2))
            square_neighbors.add((x - 1, y - 1))
            square_neighbors.add((x - 1, y))
            square_neighbors.add((x, y - 2))
            square_neighbors.add((x, y - 1))
    return square_neighbors


def constraint(var1, val1, var2, val2):
    """
    no variables of a constraint can be the same
    :param var1:
    :param val1:
    :param var2:
    :param val2:
    :return:
    """
    return val1 != val2


def build_csp(puzzle):
    """
    Create a CSP object representing the puzzle.
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: CSP object
    """
    # Enter your code here and remove the pass statement below
    return csp.CSP(build_domain(puzzle), build_neighbors(puzzle), constraint)


def q1(puzzle):
    """
    Solve the given puzzle with basic backtracking search
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: a tuple consisting of a solution (dictionary) and the
    CSP object.
    """
    # Enter your code here and remove the pass statement below
    csp1 = build_csp(puzzle)
    solution = csp1.backtracking_search()
    solution_and_csp = (solution, csp1)
    return solution_and_csp


def q2(puzzle):
    """
    Solve the given puzzle with backtracking search and AC-3 as
    a preprocessing step.
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: a tuple consisting of a solution (dictionary) and the
    CSP object.
    """
    # Enter your code here and remove the pass statement below
    csp_q2 = build_csp(puzzle)
    csp_q2.ac3_algorithm()
    solution = csp_q2.backtracking_search()
    solution_and_csp = (solution, csp_q2)
    return solution_and_csp


def q3(puzzle):
    """
    Solve the given puzzle with backtracking search and MRV ordering and
    AC-3 as a preprocessing step.
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: a tuple consisting of a solution (dictionary) and the
    CSP object.
    """
    # Enter your code here and remove the pass statement below
    csp_q3 = build_csp(puzzle)
    csp_q3.ac3_algorithm()
    solution = csp_q3.backtracking_search("MRV")
    solution_and_csp = (solution, csp_q3)
    return solution_and_csp
