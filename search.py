#!/usr/bin/env python3
"""
search.py

Generic search routines for BFS, DFS, UCS, A*,
extended from an 8-puzzle example.

We'll mark changes for Sprints with comment blocks.
"""

import util

class SearchProblem:
    """
    Abstract class: outlines the structure of a search problem.
    """

    def getStartState(self):
        util.raiseNotDefined()

    def isGoalState(self, state):
        util.raiseNotDefined()

    def getSuccessors(self, state):
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Hard-coded path for a toy maze - not used for puzzle.
    """
    return []

#############################
# /*=====Start Change Task 4=====*/
#############################
# We'll unify BFS, DFS, and A*, and in #4 compare them with the best heuristic.

def depthFirstSearch(problem):
    """
    DFS (LIFO) stack
    """
    frontier = util.Stack()
    visited = set()

    # Start node: (state, path)
    start_state = problem.getStartState()
    start_node = (start_state, [])
    frontier.push(start_node)
    max_fringe = 0

    while not frontier.isEmpty():
        # Track max fringe size
        current_size = frontier.size()
        if current_size > max_fringe:
            max_fringe = current_size

        state, path = frontier.pop()
        # Each pop is a node expansion
        problem.expanded_nodes += 1

        if problem.isGoalState(state):
            # Update the problem's max_fringe if needed
            problem.max_fringe = max(problem.max_fringe, max_fringe)
            return path

        if state not in visited:
            visited.add(state)
            for (succ, action, cost) in problem.getSuccessors(state):
                if succ not in visited:
                    new_path = path + [action]
                    frontier.push((succ, new_path))

    # Update final max fringe
    problem.max_fringe = max(problem.max_fringe, max_fringe)
    return []  # No solution found

def breadthFirstSearch(problem):
    """
    BFS (FIFO) queue
    """
    from collections import deque
    frontier = util.Queue()
    visited = set()

    # Start node: (state, path)
    start_state = problem.getStartState()
    start_node = (start_state, [])
    frontier.push(start_node)
    max_fringe = 0

    while not frontier.isEmpty():
        current_size = frontier.size()
        if current_size > max_fringe:
            max_fringe = current_size

        state, path = frontier.pop()
        problem.expanded_nodes += 1

        if problem.isGoalState(state):
            problem.max_fringe = max(problem.max_fringe, max_fringe)
            return path

        if state not in visited:
            visited.add(state)
            for (succ, action, cost) in problem.getSuccessors(state):
                if succ not in visited:
                    new_path = path + [action]
                    frontier.push((succ, new_path))

    problem.max_fringe = max(problem.max_fringe, max_fringe)
    return []

def uniformCostSearch(problem):
    """
    UCS: priority queue ordered by path cost.
    """
    frontier = util.PriorityQueue()
    visited = {}  # state -> best cost so far

    start_state = problem.getStartState()
    start_node = (start_state, [], 0)  # (state, path, cost_so_far)
    frontier.push(start_node, 0)
    max_fringe = 0

    while not frontier.isEmpty():
        current_size = frontier.size()
        if current_size > max_fringe:
            max_fringe = current_size

        state, path, cost_so_far = frontier.pop()
        problem.expanded_nodes += 1

        if problem.isGoalState(state):
            problem.max_fringe = max(problem.max_fringe, max_fringe)
            return path

        if (state not in visited) or (cost_so_far < visited[state]):
            visited[state] = cost_so_far
            for (succ, action, step_cost) in problem.getSuccessors(state):
                new_path = path + [action]
                new_cost = cost_so_far + step_cost
                if (succ not in visited) or (new_cost < visited[succ]):
                    frontier.update((succ, new_path, new_cost), new_cost)

    problem.max_fringe = max(problem.max_fringe, max_fringe)
    return []

def nullHeuristic(state, problem=None):
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """
    A* = UCS + heuristic
    """
    frontier = util.PriorityQueue()
    visited = {}
    start_state = problem.getStartState()
    start_node = (start_state, [], 0)  # (state, path, cost_g)
    frontier.push(start_node, 0)
    max_fringe = 0

    while not frontier.isEmpty():
        current_size = frontier.size()
        if current_size > max_fringe:
            max_fringe = current_size

        state, path, cost_g = frontier.pop()
        problem.expanded_nodes += 1

        if problem.isGoalState(state):
            problem.max_fringe = max(problem.max_fringe, max_fringe)
            return path

        if (state not in visited) or (cost_g < visited[state]):
            visited[state] = cost_g
            for (succ, action, step_cost) in problem.getSuccessors(state):
                new_path = path + [action]
                new_g = cost_g + step_cost
                new_f = new_g + heuristic(succ, problem)
                if (succ not in visited) or (new_g < visited[succ]):
                    frontier.update((succ, new_path, new_g), new_f)

    problem.max_fringe = max(problem.max_fringe, max_fringe)
    return []

#############################
# /*=====End Change Task 4=====*/
#############################

# Abbreviations
bfs  = breadthFirstSearch
dfs  = depthFirstSearch
ucs  = uniformCostSearch
astar= aStarSearch
