# ----------------------------------------------------------------------
# Name:     adversarial_search
# Purpose:  Homework 6 - Implement adversarial search algorithms
#
# Author: Byron O'Gorman
#
# ----------------------------------------------------------------------
"""
Adversarial search algorithms implementation

Your task for homework 6 is to implement:
1.  minimax
2.  alphabeta
3.  abdl (alpha beta depth limited)
"""
import random
import math  # You can use math.inf to initialize to infinity


def rand(state):
    """
    Generate a random move.
    :param state: GameState object
    :return:  a tuple representing the row column of the random move
    """
    done = False
    while not done:
        row = random.randint(0, state.size - 1)
        col = random.randint(0, state.size - 1)
        if state.available(row, col):
            done = True
    return row, col


def minimax(state):
    """
    Find the best move for our AI agent using the minimax algorithm.
    (searching the entire tree from the current game state)
    :param state: GameState object
    :return:  a tuple representing the row column of the best move
    """

    return max(state.possible_moves(), key=lambda tup: value(state.successor(tup, 'AI'), 'user'))


def value(state, agent):
    """
    Calculate the minimax value for any state under the given agent's
    control.
    :param state: GameState object - state may be terminal or
    non-terminal
    :param agent: (string) 'user' or 'AI' - AI is max
    :return: (integer) value of that state -1, 0 or 1
    """

    if state.is_tie():
        return 0
    if state.is_win('user'): return -1
    if state.is_win('AI'): return 1

    if agent == 'AI':  # if the agent is 'MAX'
        return max_value(state)
    else:  # else the agent is 'MIN'
        return min_value(state)


def max_value(state):
    """
    Calculate the minimax value for a non-terminal state under Max's
    control (AI agent)
    :param state: non-terminal GameState object
    :return: (integer) value of that state -1, 0 or 1
    """

    v = max(value(state.successor(s, 'AI'), 'user') for s in state.possible_moves())
    return v


def min_value(state):
    """
    Calculate the minimax value for a non-terminal state under Min's
    control (user)
    :param state: non-terminal GameState object
    :return: (integer) value of that state -1, 0 or 1
    """

    v = min(value(state.successor(s, 'user'), 'AI') for s in state.possible_moves())
    return v


def alphabeta(state):
    """
    Find the best move for our AI agent using the minimax algorithm
    with alpha beta pruning.
    :param state: GameState object
    :return:  a tuple representing the row column of the best move
    """
    # Enter your code here and remove the raise statement below
    return max(state.possible_moves(),
               key=lambda tup: ab_value(state.successor(tup, 'AI'), 'user', -math.inf, math.inf))


def ab_value(state, agent, alpha, beta):
    """
    Calculate the minimax value for any state under the given agent's
    control using alpha beta pruning
    :param state: GameState object - state may be terminal or
    non-terminal.
    :param agent: (string) 'user' or 'AI' - AI is max
    :return: (integer) value of that state -1, 0 or 1
    """
    if state.is_tie():
        return 0
    if state.is_win('user'):
        return -1
    if state.is_win('AI'):
        return 1

    if agent == 'AI':  # if the agent is 'MAX'
        return abmax_value(state, alpha, beta)
    else:  # else the agent is 'MIN'
        return abmin_value(state, alpha, beta)


def abmax_value(state, alpha, beta):
    """
    Calculate the minimax value for a non-terminal state under Max's
    control (AI agent) using alpha beta pruning
    :param state: non-terminal GameState object
    :return: (integer) value of that state -1, 0 or 1
    """
    v = -math.inf
    for move in state.possible_moves():
        v = max(v, ab_value(state.successor(move, 'AI'), 'user', alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def abmin_value(state, alpha, beta):
    """
    Calculate the minimax value for a non-terminal state under Min's
    control (user) using alpha beta pruning
    :param state: non-terminal GameState object
    :return: (integer) value of that state -1, 0 or 1
    """
    v = math.inf
    for move in state.possible_moves():
        v = min(v, ab_value(state.successor(move, 'user'), 'AI', alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v


def abdl(state, depth):
    """
    Find the best move for our AI agent by limiting the alpha beta
    search the given depth and using the evaluation function
    state.eval()
    :param state: GameState object
    :return:  a tuple representing the row column of the best move
    """
    # Enter your code here and remove the raise statement below
    return max(state.possible_moves(),
               key=lambda tup: abdl_value(state.successor(tup, 'AI'), 'user', -math.inf, math.inf, depth))


def abdl_value(state, agent, alpha, beta, depth):
    """
    Calculate the utility for any state under the given agent's control
    using depth limited alpha beta pruning and the evaluation
    function state.eval()
    :param state: GameState object - state may be terminal or
    non-terminal
    :param agent: (string) 'user' or 'AI' - AI is max
    :return: (integer) utility of that state
    """
    # if the state is a terminal state: return the state's utility
    if state.is_win('AI'):
        return (state.size ** 2) - 1
    if state.is_tie():
        return 0
    if state.is_win('user'):
        return -(state.size ** 2) - 1
    # if max depth is reached, return the states estimated utility
    if depth == 0:
        return state.eval()
    if agent == 'AI':  # if the agent is 'MAX'
        return abdlmax_value(state, alpha, beta, depth)
    else:  # else the agent is 'MIN'
        return abdlmin_value(state, alpha, beta, depth)


def abdlmax_value(state, alpha, beta, depth):
    """
    Calculate the utility for a non-terminal state under Max's control
    using depth limited alpha beta pruning and the evaluation
    function state.eval()
    :param state: non-terminal GameState object
    :return: (integer) utility (evaluation function) of that state
    """
    v = -math.inf
    for move in state.possible_moves():
        v = max(v, abdl_value(state.successor(move, 'AI'), 'user', alpha, beta, depth - 1))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def abdlmin_value(state, alpha, beta, depth):
    """
    Calculate the utility for a non-terminal state under Min's control
    using depth limited alpha beta pruning and the evaluation
    function state.eval()
    :param state: non-terminal GameState object
    :return: (integer) utility (evaluation function) of that state
    """
    v = math.inf
    for move in state.possible_moves():
        v = min(v, abdl_value(state.successor(move, 'user'), 'AI', alpha, beta, depth - 1))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v
