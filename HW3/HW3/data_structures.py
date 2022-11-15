"""
Class definitions for data structures used by the search algorithms
"""
import heapq  # for the priority queue implementation


class Node(object):
    """
    Represent a a node in the search tree/graph.
    Arguments:
    state:  problem state corresponding to this node - defaults to None
    parent: the parent Node object corresponding to the predecessor
        state or None if root node.
    action: the action that got us to the current state or None if root.
    cumulative_cost: the cumulative total cost from the root to the
        current state - defaults to 0.
    Attributes:
    parent: the parent Node object corresponding to the predecessor
        state or None if root node.
    action: the action that got us to the current state or None if root.
    cumulative_cost: the cumulative total cost from the root to the
        current state
    """

    def __init__(self, state, parent, action, cumulative_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cumulative_cost = cumulative_cost  # cost from root

    def solution(self):
        """
        Returns the sequence of actions from the root to this node
        :return: list of actions
        """
        return [node.action for node in self._node_path()[1:]]

    def _node_path(self):
        """
        Returns list of nodes from the root to this node.
        This is a private method.  Please do not use it.
        :return: list of Node objects
        """
        node = self
        path = []
        while node:
            path.append(node)
            node = node.parent
        path.reverse()
        return path


class Stack(object):
    """
    Represent a stack with LIFO (last in first out) queuing
    """

    def __init__(self):
        self.list = []

    def push(self, item):
        """
        Push the given item on the stack
        :param item: (of any type)
        :return: None
        """
        self.list.append(item)

    def pop(self):
        """
        Remove the most recently pushed item from the stack and return it.
        :return: item (of any type)
        """
        return self.list.pop()

    def is_empty(self):
        """
        Is this stack empty?
        :return: (Boolean) True if the stack is empty, False otherwise
        """
        return not self.list


class Queue:
    """
    Represent a queue with FIFO (first in first out) queuing
    """

    def __init__(self):
        self.list = []

    def push(self, item):
        """
        Add the given item to the end of the queue
        :param item: (of any type)
        :return: None
        """
        self.list.insert(0, item)

    def pop(self):
        """
        Remove the earliest pushed item from the queue and return it.
        :return: item (of any type)
        """
        return self.list.pop()

    def is_empty(self):
        """
        Is this queue empty?
        :return: (Boolean) True if the queue is empty, False otherwise
        """
        return not self.list


class PriorityQueue(object):
    """
    Represent a priority queue container where each item has a priority
    associated with it.
    """

    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        """
        Add the given item with the given priority to the queue
        :param
        item: (of any type)
        priority: (number or other orderable type)
        :return: None
        """
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        """
        Remove the item with the lowest priority from the queue and return it.
        :return: item (of any type)
        """
        priority, count, item = heapq.heappop(self.heap)
        return item

    def is_empty(self):
        """
        Is this priority queue empty?
        :return: (Boolean) True if the queue is empty, False otherwise
        """
        return not self.heap
