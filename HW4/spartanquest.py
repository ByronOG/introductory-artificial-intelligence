# ----------------------------------------------------------------------
# Name:    spartanquest
# Purpose: Illustrate advantages and limitations of search algorithms
#
# Author:   Rula Khayrallah
#
# Copyright ©  Rula Khayrallah
# ----------------------------------------------------------------------
"""
Main program to guide Sammy the Spartan on a quest within a given maze

Usage:  spartanquest.py maze_file search_algorithm
The maze_file is a text file such as SJSU.txt
The search_algorithm in homework 3 is:
    dfs: for depth first search
    bfs: for breadth first search
    ucs for uniform cost search
The search_algorithm in homework 4 is:
    astar: for A*  search

Example:  spartanquest.py SJSU.txt dfs

The uninformed search algorithms functions are implemented in the file
uninformed_search.py.

Your task for homework 4 is to implement astar in informed_search.py.

"""
import time
import argparse
import uninformed_search
import informed_search
import graphics

class Maze(object):
    """
    Represent the maze layout: its width, height and walls

    Arguments:
    width (int):  the width of the maze
    height (int): the height of the maze

    Attributes:
    width (int):  the width of the maze
    height (int): the height of the maze
    walls (two dimensional list of booleans):
        Each element represents a position in the maze.
        True indicates that there is a wall in that position.
        False indicates the absence of a wall.
        self.walls[x][y] indicates the presence or absence of a wall
        at position (x, y) in the maze.
    """
    def __init__(self, width, height):
        self.walls = [[False for x in range(width)]
                      for y in range(height)]
        self.width = width
        self.height = height

    def add_wall(self, position):
        """
        Add a wall in the specified position
        :param position: tuple(row, column) representing a maze position
        :return: None
        """
        x, y = position
        self.walls[y][x] = True

    def is_wall(self, position):
        """
        Is there a wall in the given position?
        :param position: tuple(row, column) representing a maze position
        :return: (Boolean) True if there is a wall in that position,
        False otherwise
        """
        x, y = position
        return self.walls[y][x]

    def within_bounds(self, position):
        """
        Is the given position within the maze?
        :param position: tuple (row, column) representing a position
        :return: (Boolean) True if the position is inside the maze,
        False otherwise
        """
        x, y = position
        return (0 <= x <= self.width -1) and (0 <= y <= self.height - 1)


class Problem(object):
    """
    Represent our search problem at any point in the quest

    Arguments:
    mazefile (file): text file containing the maze info

    Attributes:
    maze (Maze object):  the maze for this quest
    The maze is constant throughout the quest
    mascot_position (tuple of integers): the current position of Sammy
    medals (a set of tuples): a set containing the positions of the
    remaining medals in the quest
    """
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"
    moves = {EAST: (1, 0), WEST: (-1, 0), SOUTH: (0, 1), NORTH: (0, -1)}

    # The cost (number of carrots consumed) associated with each move.
    cost = {EAST: 15, WEST: 1, SOUTH: 2, NORTH: 14}

    def __init__(self, mazefile):
        self._nodes_expanded = 0 # private variable
        self.medals = set()
        self.read_quest(mazefile)

    def read_quest(self, mazefile):
        """
        Read the maze file specified and save the information in a Maze
        object.
        The length of the first line in the file is used to determine
        the width of the maze.  So the last position in the first row of
        the maze must be represented by a character in the first line
        (not a space).
        W or w:  represent a wall
        M or m: represent the presence of a medal at that position
        S or s: represent the starting position of our mascot Sammy
        Any other character: a vacant maze position
        :param
        mazefile (file object): the file object containing the maze info
        :return: None
        """
        layout = mazefile.readlines()
        width = len(layout[0].strip()) # the first line
        height = len(layout) # the number of lines represents the height
        self.maze = Maze(width, height)
        y = 0
        for line in layout:
            x = 0
            for char in line:
                if char in {'W', 'w'}: # W represents a wall
                    self.maze.add_wall((x, y))
                elif char in {'M', 'm'}: # M represents a medal position
                    self.add_medal((x, y))
                elif char in {'S', 's'}: # S represents Sammy's position
                    self.add_mascot((x, y))
                x += 1 # anything else is a vacant maze position
            y += 1
        mazefile.close()


    def add_mascot(self, position):
        """
        Save the mascot's position
        :param position: tuple (row,column) representing a maze position
        :return: None
        """
        self.mascot_position = position

    def add_medal(self, position):
        """
        Add the specified position to the set containing all the medals
        :param position: tuple (x, y) representing a maze position
        :return: None
        """
        self.medals.add(position)

    def is_goal(self, state):
        """
        Is the state specified a goal state?
        The state is a goal state when there are no medals left to
        collect.
        :param
        state - A state is represented by a tuple containing two tuples:
                the current position (x, y) of Sammy the Spartan
                a tuple containing the positions of the remaining medals

        :return: Boolean - True if this is a goal state, False otherwise
        """
        position, medals_left = state
        return not medals_left

    def start_state(self):
        """
        Return the start state in this quest
        The start state is identified by the mascot's position and the
        initial distribution of the medals in the maze.
        It is represented by a tuple containing two other tuples:
                the current position (x, y) of Sammy the Spartan
                a tuple containing the positions of the medals

        :return:
        state - The start state in the quest
                A state is represented by a tuple containing two tuples:
                the current position (row, column) of Sammy the Spartan
                a tuple containing the positions of the remaining medals
        """
        return self.mascot_position, tuple(self.medals)

    def expand(self, state):
        """
        Return a list of tuples representing all states reachable
        from the current state with their corresponding action and costs
        :param
        state - A state is represented by a tuple containing two other tuples:
                the current position (x, y) of Sammy the Spartan
                a tuple containing the positions of the remaining medals
        :return:
        a list of tuples representing all states that are reachable
        from the current state with their corresponding action and cost
        """
        result = []
        self._nodes_expanded += 1 # update private variable
        position, current_medals = state
        current_x, current_y = position
        for action in self.moves:
            new_position = (current_x + self.moves[action][0],
                            current_y + self.moves[action][1])
            # if the move in that direction is valid
            if self.maze.within_bounds(new_position) and \
                not self.maze.is_wall(new_position):
                new_medals = set(current_medals) - {new_position}
                new_state = (new_position, tuple(new_medals))
                result.append((new_state, action, self.cost[action]))
        return result


    def path_cost(self, actions):
        """
        Return the total cost of a sequence of actions/moves
        :param
        actions (list) - A list of actions/moves
        :return (int):  the total cost of these actions
        """
        return sum(self.cost[action] for action in actions)

    def nodes_expanded(self):
        return self._nodes_expanded


def get_arguments():
    '''
    Parse and validate the command line arguments
    :return: (tuple containing a file object and a string)
            the maze file specified  and the search algoeithm specified
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('maze_file',
                        help='name of the text file containing the maze info',
                        type=argparse.FileType('r')) # open the file
    parser.add_argument('search_algorithm',
                        help='astar, dfs, bfs or ucs?',
                        choices=['astar','dfs', 'bfs', 'ucs'])
    parser.add_argument('heuristic',
                        help='A* heuristic',
                        nargs='?',
                        default='null_heuristic')
    arguments = parser.parse_args()

    maze_file = arguments.maze_file
    search = arguments.search_algorithm
    heuristic = arguments.heuristic
    return maze_file, search, heuristic

def main():
    maze_file, search, heuristic = get_arguments()
    quest = Problem(maze_file)  # Initialize our search problem for this quest
    start_time = time.time()
    if search == "astar":
        heuristic_function = getattr(informed_search, heuristic)
        search_function = getattr(informed_search, search)
        solution = search_function(quest, heuristic_function)
    else:
        search_function = getattr(uninformed_search, search)
        solution = search_function(quest)  # Invoke the search algorithm
    elapsed_time = time.time() - start_time

    # Print some statistics
    if solution is not None:
        print('Path length: ', len(solution))
        print('Carrots consumed: ', quest.path_cost(solution))
    else:
        print('The quest failed!')
    print(f'Number of nodes expanded: {quest.nodes_expanded():,}')
    print(f'Processing time: {elapsed_time:.4f}(sec)')

    graphics.Display(quest, solution)  # Visualize the solution


if __name__ == '__main__':
    main()