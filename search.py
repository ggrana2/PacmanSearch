# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util


class Node:

    def __init__(self, state, successor, action, cost):
        self.state = state
        self.successor = successor
        self.action = action
        self.cost = cost


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions. The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    visited = set()
    path = []
    path2curr = util.Stack()
    fringe = util.Stack()
    fringe.push(problem.getStartState())
    while not fringe.isEmpty():
        # pop random successor
        currstate = fringe.pop()
        if problem.isGoalState(currstate):
            return path
        # check if visited node already
        if currstate not in visited:
            visited.add(currstate)
            # expand node
            successors = problem.getSuccessors(currstate)
            # put successors on fringe
            for successor in successors:
                if successor[0] not in visited:
                    fringe.push(successor[0])
                    # push path to all nodes visited
                    path2curr.push(path + [successor[1]])
            # last node visited will be goal node, so return it
        path = path2curr.pop()
    return path

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"

    visited = []
    path = []
    path2curr = util.Queue()
    fringe = util.Queue()
    fringe.push(problem.getStartState())
    while not fringe.isEmpty():
        # pop random successor
        currstate = fringe.pop()
        if problem.isGoalState(currstate):
            return path
        # check if visited node already
        if currstate not in visited:
            visited.append(currstate)
            # expand node
            successors = problem.getSuccessors(currstate)
            # put successors on fringe
            for successor in successors:
                if successor[0] not in visited:
                    fringe.push(successor[0])
                    # push path to all nodes visited
                    path2curr.push(path + [successor[1]])
            # last node visited will be goal node, so return it
        path = path2curr.pop()
    return path

    util.raiseNotDefined()


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    visited = set()
    path = []
    path2curr = util.PriorityQueue()
    fringe = util.PriorityQueue()
    start = (problem.getStartState(), 0, 0)
    fringe.push(start, 0)
    while not fringe.isEmpty():
        # pop random successor
        currstate = fringe.pop()
        if problem.isGoalState(currstate[0]):
            return path
        # check if visited node already
        if currstate[0] not in visited:
            visited.add(currstate[0])
            successors = problem.getSuccessors(currstate[0])
            for successor in successors:  # tuple: state, action, cost
                state, action, cost = successor
                if state not in visited:
                    costFromStart = problem.getCostOfActions(path + [action])
                    fringe.push(successor, costFromStart)  # push entire successor with it's priority
                    path2curr.push(path + [action], costFromStart)
        path = path2curr.pop()
    return path


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"

    visited = set()
    path = []
    path2curr = util.PriorityQueue()
    fringe = util.PriorityQueue()
    start = (problem.getStartState(), 0, 0)
    print("start state: ", start[0])
    fringe.push(start[0], 0)
    while not fringe.isEmpty():
        # pop random successor
        currstate = fringe.pop()

        print("currstate length: ", type(currstate))
        print("currstate: ", currstate)

        if problem.isGoalState(currstate):
            return path
        state = tuple(currstate)
        if state not in visited:
            visited.add(tuple(currstate))
            successors = problem.getSuccessors(currstate)
            for successor in successors:  # tuple: state, action, cost
                state, action, cost = successor
                succHeur = heuristic(state, problem)
                if state not in visited:
                    costFromStart = problem.getCostOfActions(path + [action])
                    fringe.push(state, costFromStart + succHeur)  # push entire successor with it's priority
                    path2curr.push(path + [action], costFromStart + succHeur)
        path = path2curr.pop()
    return path


    # I'VE INCLUDED MY IMPLEMENTATION USING A SET THAT WORKS FOR ALL MY SEARCH AGENTS AND HEURISTICS EXCEPT THE CORNER ONE
    # DUE TO THE WAY THAT IT IS STRUCTURED.

    #
    # visited = set()
    # path = []
    # path2curr = util.PriorityQueue()
    # fringe = util.PriorityQueue()
    # start = (problem.getStartState(), 0, 0)
    # print("start state: ", start[0])
    # fringe.push(start[0], 0)
    # while not fringe.isEmpty():
    #     # pop random successor
    #     currstate = fringe.pop()
    #
    #     print("currstate length: ", len(currstate))
    #     print("currstate: ", currstate)
    #
    #     if problem.isGoalState(currstate):
    #         return path
    #
    #     if currstate not in visited:
    #         visited.add(currstate)
    #         successors = problem.getSuccessors(currstate)
    #         for successor in successors:  # tuple: state, action, cost
    #             state, action, cost = successor
    #             succHeur = heuristic(state, problem)
    #             if state not in visited:
    #                 costFromStart = problem.getCostOfActions(path + [action])
    #                 fringe.push(state, costFromStart + succHeur)  # push entire successor with it's priority
    #                 path2curr.push(path + [action], costFromStart + succHeur)
    #     path = path2curr.pop()
    # return path



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
