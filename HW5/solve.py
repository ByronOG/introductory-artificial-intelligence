# ----------------------------------------------------------------------
# Name:     solve
# Purpose:  homework 5
#
# Author:   Rula Khayrallah
#
# Copyright ©  Rula Khayrallah, 2019
# ----------------------------------------------------------------------
"""
Main module to read and solve a Sudoku puzzle.

Usage:  solve.py question puzzle_file
question corresponds to the question number in Homework 5 and the
function name in the sudoku module: q1, q2 or q3
puzzle_file is a text file such as easy.txt
Example:  solve.py q1 veryeasy.txt
"""

import argparse
import time
import sudoku

def read_puzzle(puzzle_file):
    """
    Read the puzzle file and return a dictionary
    :param puzzle_file: (file object) representing the Sudoku puzzle
    :return: dictionary: The dictionary keys are tuples (row, column)
        representing the filled puzzle squares and the values are
        the corresponding numbers assigned to these squares.
    """
    puzzle = {}
    row = 0
    for line in puzzle_file:
        column = 0
        for char in line.strip():
            if char != '?':
                puzzle[(row, column)] = int(char)
            column += 1
        row += 1
    # to see exactly what is returned, print(puzzle)
    return puzzle


def write_solution(assignment):
    """
    Print the puzzle solution.
    :param solution: a dictionary representing  the puzzle solution.
        The dictionary keys are tuples (row, column) and the values are
        singleton sets containing the value corresponding to that
        row and column.
    :return: None
    """
    if assignment is not None:
            for row in range(9):
                for col in range(9):
                    if (row, col) in assignment:
                        print(assignment[row, col], sep='', end='')
                print()

def get_arguments():
    '''
    Parse and validate the command line arguments
    :return: (tuple containing a file object and a string)
            the maze file specified  and the search algoeithm specified
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('question',
                        help='q1, q2 or q3?',
                        choices = ['q1', 'q2', 'q3'])
    parser.add_argument('puzzle_file',
                        help='name of the text file containing the puzzle?',
                        type=argparse.FileType('r')) # open the file

    arguments = parser.parse_args()

    puzzle_file = arguments.puzzle_file
    question = arguments.question
    return question, puzzle_file

def main():
    question, puzzle_file = get_arguments()
    puzzle = read_puzzle(puzzle_file)
    question_function = getattr(sudoku, question)
    start_time = time.time()
    solution, csp = question_function(puzzle)
    elapsed_time = time.time() - start_time
    print('Processing time: {:.4f} (sec)'.format(elapsed_time))
    print (f'Nodes Expanded: {csp._nodes:,}')
    if solution is not None:
            for row in range(9):
                for col in range(9):
                    if (row, col) in solution:
                        print(solution[row, col], sep='', end='')
                print()
    else:
        print("Unable to solve the puzzle.")


if __name__ == '__main__':
    main()