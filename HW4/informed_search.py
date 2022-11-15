# ----------------------------------------------------------------------
# Name:     informed_search
# Purpose:  Homework 4 - Implement astar and some heuristics
#
# Author(s):
# ----------------------------------------------------------------------
"""
A* Algorithm and heuristics implementation

Your task for homework 4 is to implement:
1.  astar
2.  single_heuristic
3.  better_heuristic
4.  gen_heuristic
"""
import data_structures


def astar(problem, heuristic):
    """
    A* graph search algorithm
    returns a solution for the given search problem
    :param
    problem (a Problem object) representing the quest
            see Problem class definition in spartanquest.py
    heuristic (a function) the heuristic function to be used
    :return: list of actions representing the solution to the quest
                or None if there is no solution
    """
    # Enter your code here and remove the pass statement below
    closed = set()  # keep track of our explored states
    fringe = data_structures.PriorityQueue()  # for ucd, the fringe is a priority queue
    state = problem.start_state()
    root = data_structures.Node(state, None, None)
    fringe.push(root, root.cumulative_cost)
    while not fringe.is_empty():
        node = fringe.pop()
        if problem.is_goal(node.state):
            return node.solution()  # we found a solution
        if node.state not in closed:  # we are implementing graph search
            closed.add(node.state)
            for child_state, action, action_cost in problem.expand(node.state):  # add action cost to cumulative cost
                child_node = data_structures.Node(child_state, node, action, node.cumulative_cost + action_cost)
                fringe.push(child_node,
                            child_node.cumulative_cost + heuristic(child_state, problem))  # add new node to PQ
    return None  # Failure -  no solution was found


def null_heuristic(state, problem):
    """
    Trivial heuristic to be used with A*.
    Running A* with this null heuristic, gives us uniform cost search
    :param
    state: A state is represented by a tuple containing:
                the current position of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest
    :return: 0
    """
    return 0


def manhattan_distance(position1, position2):
    """
    Function to calculate the manhattan distance between two positions
    :param
    position1: position1 is represented by a tuple
    position2: position2 is represented by a tuple

    :return: int
    """
    x1, y1 = position1
    x2, y2 = position2

    x_distance = abs(x1 - x2)
    y_distance = abs(y1 - y2)
    return x_distance + y_distance


def single_heuristic(state, problem):
    """
    return the manhattan distance between sammy and the medal as the heuristic
    * only calculated if one medal remains in the problem
    It is admissible as the returned value is less than the true distance
    :param
    state: A state is represented by a tuple containing:
                the current position of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest

    :return: int
    """
    # Enter your code here and remove the pass statement below
    sammy_pos, remaining_medals = state
    if len(remaining_medals) == 1:
        medal, = remaining_medals
        return manhattan_distance(sammy_pos, medal)
    else:
        return 0


def direction(position1, position2, problem):
    """
    calculate the direction of the distance between Sammy and the medal
    return the total cost of the two directions
    :param
    problem: (a Problem object) representing the quest
    position1: sammy's position
    position2: medal's position

    :return: int
    """

    x1, y1 = position1
    x2, y2 = position2
    x_dir = x1 - x2
    y_dir = y1 - y2
    total = 0
    if x_dir < 0:
        total += problem.cost["E"]
    if y_dir > 0:
        total += problem.cost["N"]
    if y_dir < 0:
        total += problem.cost["S"]
    return total


def x_cost(sammy_pos, medal_pos, problem):
    x1 = sammy_pos[0]
    x2 = medal_pos[0]
    x_direction = x1-x2
    if x_direction < 0:
        return abs(x_direction) * problem.cost["E"]
    else:
        return abs(x_direction) * problem.cost["W"]


def y_cost(sammy_pos, medal_pos, problem):
    y1 = sammy_pos[1]
    y2 = medal_pos[1]
    y_direction = y1-y2
    if y_direction < 0:
        return abs(y_direction) * problem.cost["S"]
    else:
        return abs(y_direction) * problem.cost["N"]


def better_heuristic(state, problem):
    """
    calculate the manhattan distance and multiply it by the cost of the directions taken
    It is admissible as the returned value is less than the true cost
    :param
    state: A state is represented by a tuple containing:
                the current position of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest

    :return: int
    """
    # Enter your code here and remove the pass statement below
    sammy_pos, remaining_medals = state
    if not problem.is_goal(state):
        medal, = remaining_medals
        return x_cost(sammy_pos, medal, problem) + y_cost(sammy_pos, medal, problem)
    else:
        return 0


def gen_heuristic(state, problem):
    """
    Find the minimum cost for sammy to reach a medal
    It is admissible as the returned value is less than the true cost
    :param
    state: A state is represented by a tuple containing:
                the current position of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest

    :return: int
    """
    # Enter your code here and remove the pass statement below
    sammy, medals = state
    # return min([manhattan_distance(sammy, medal)*direction(sammy, medal, problem) for medal in medals], default=0)
    return max((x_cost(sammy, medal, problem)+y_cost(sammy, medal, problem) for medal in medals), default=0)
