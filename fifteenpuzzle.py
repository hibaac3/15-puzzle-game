#!/usr/bin/env python3
"""
fifteenpuzzle.py

Modified from an 8-puzzle example to handle a 15-puzzle (4x4 grid).
Blank tile is 0, located in bottom-right for the goal state.

We mark each sprint's changes using special comment blocks.
"""

import random
import search
import time

########################
# /*=====Start Change Task 1=====*/
########################
# SPRINT #1: Convert from 8-puzzle to 15-puzzle, blank in bottom-right.

class FifteenPuzzleState:
    """
    Represents a 4x4 sliding puzzle with tiles 1..15 plus blank=0.
    The goal state is:
       1   2   3   4
       5   6   7   8
       9  10  11  12
      13  14  15   0
    """

    def __init__(self, numbers):
        """
        numbers: list or tuple of length 16, containing numbers 0..15.
        """
        if len(numbers) != 16:
            raise ValueError("FifteenPuzzleState needs exactly 16 numbers (0..15).")
        self.size = 4
        self.cells = []
        idx = 0
        for r in range(self.size):
            row_list = []
            for c in range(self.size):
                row_list.append(numbers[idx])
                idx += 1
            self.cells.append(row_list)

        # locate the blank tile (0)
        for r in range(self.size):
            for c in range(self.size):
                if self.cells[r][c] == 0:
                    self.blankLocation = (r, c)
                    break

    def isGoal(self):
        """
        Checks whether the puzzle is in the goal configuration.
        Goal: 1..15 in row-major order with 0 in the bottom-right.
        """
        correct_val = 1
        for r in range(self.size):
            for c in range(self.size):
                if (r, c) == (self.size - 1, self.size - 1):
                    if self.cells[r][c] != 0:
                        return False
                else:
                    if self.cells[r][c] != correct_val:
                        return False
                    correct_val += 1
        return True

    def legalMoves(self):
        """
        Returns a list of legal moves: 'up', 'down', 'left', and 'right'.
        """
        moves = []
        r, c = self.blankLocation
        if r > 0:
            moves.append('up')
        if r < self.size - 1:
            moves.append('down')
        if c > 0:
            moves.append('left')
        if c < self.size - 1:
            moves.append('right')
        return moves

    def result(self, move):
        """
        Returns a new FifteenPuzzleState with the blank moved in the given direction.
        """
        r, c = self.blankLocation
        if move == 'up':
            nr, nc = r - 1, c
        elif move == 'down':
            nr, nc = r + 1, c
        elif move == 'left':
            nr, nc = r, c - 1
        elif move == 'right':
            nr, nc = r, c + 1
        else:
            raise ValueError("Invalid move: " + move)

        # Flatten the cells for easy swapping
        flat = [cell for row in self.cells for cell in row]
        blank_idx = r * self.size + c
        swap_idx = nr * self.size + nc
        flat[blank_idx], flat[swap_idx] = flat[swap_idx], flat[blank_idx]
        return FifteenPuzzleState(flat)

    def __eq__(self, other):
        return self.cells == other.cells

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.cells))

    def __str__(self):
        lines = []
        lines.append("-" * 19)
        for row in self.cells:
            row_str = []
            for val in row:
                if val == 0:
                    row_str.append("  ")
                else:
                    row_str.append(f"{val:2d}")
            lines.append("| " + " ".join(row_str) + " |")
        lines.append("-" * 19)
        return "\n".join(lines)

def createRandomFifteenPuzzle(moves=50):
    """
    Creates a random 15-puzzle by starting from the goal configuration and applying
    a number of random legal moves.
    
    Increasing the number of moves (e.g., 50) creates a harder puzzle.
    """
    # Goal configuration: [1,2,...,15,0]
    initial = list(range(1, 16)) + [0]
    puzzle = FifteenPuzzleState(initial)
    for _ in range(moves):
        possible = puzzle.legalMoves()
        chosen = random.choice(possible)
        puzzle = puzzle.result(chosen)
    return puzzle

class FifteenPuzzleSearchProblem(search.SearchProblem):
    """
    Wraps a FifteenPuzzleState into a search problem.
    Also maintains counters for expanded nodes and maximum fringe size.
    """
    def __init__(self, puzzleState):
        self.startState = puzzleState
        self.expanded_nodes = 0
        self.max_fringe = 0

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        return state.isGoal()

    def getSuccessors(self, state):
        succs = []
        for move in state.legalMoves():
            next_state = state.result(move)
            succs.append((next_state, move, 1))  # Each move costs 1
        return succs

    def getCostOfActions(self, actions):
        return len(actions)
########################
# /*=====End Change Task 1=====*/
########################


########################
# /*=====Start Change Task 2=====*/
########################
# SPRINT #2: Implement four admissible heuristics (h1, h2, h3, h4).

def h1_misplacedTiles(state, problem=None):
    """
    h1: Counts the number of tiles not in the correct position.
    """
    size = 4
    count = 0
    goal_val = 1
    for r in range(size):
        for c in range(size):
            if r == size - 1 and c == size - 1:
                if state.cells[r][c] != 0:
                    count += 1
            else:
                if state.cells[r][c] != goal_val:
                    count += 1
                goal_val += 1
    return count

def h2_euclideanDistance(state, problem=None):
    """
    h2: Returns the sum of Euclidean distances of each tile from its goal position.
    """
    dist_sum = 0
    size = 4
    for r in range(size):
        for c in range(size):
            val = state.cells[r][c]
            if val != 0:
                goal_r = (val - 1) // size
                goal_c = (val - 1) % size
                dist_sum += ((r - goal_r)**2 + (c - goal_c)**2)**0.5
    return dist_sum

def h3_manhattanDistance(state, problem=None):
    """
    h3: Returns the sum of Manhattan distances of each tile from its goal position.
    """
    dist_sum = 0
    size = 4
    for r in range(size):
        for c in range(size):
            val = state.cells[r][c]
            if val != 0:
                goal_r = (val - 1) // size
                goal_c = (val - 1) % size
                dist_sum += abs(r - goal_r) + abs(c - goal_c)
    return dist_sum

def h4_rowColDifference(state, problem=None):
    """
    h4: Returns the number of tiles out of their correct row plus those out of their correct column.
    """
    size = 4
    out_row = 0
    out_col = 0
    for r in range(size):
        for c in range(size):
            val = state.cells[r][c]
            if val != 0:
                goal_r = (val - 1) // size
                goal_c = (val - 1) % size
                if r != goal_r:
                    out_row += 1
                if c != goal_c:
                    out_col += 1
    return out_row + out_col
########################
# /*=====End Change Task 2=====*/
########################


def demoTest():
    puzzle = createRandomFifteenPuzzle(moves=50)
    print("Random 15-puzzle (harder):\n", puzzle)
    problem = FifteenPuzzleSearchProblem(puzzle)

    import search
    heuristics = [
        (h1_misplacedTiles, "h1_misplaced"),
        (h2_euclideanDistance, "h2_euclid"),
        (h3_manhattanDistance, "h3_manhattan"),
        (h4_rowColDifference, "h4_rowCol")
    ]

    for (hfn, name) in heuristics:
        print(f"\nUsing {name} ...")

        # Reset counters for each heuristic
        problem.expanded_nodes = 0
        problem.max_fringe = 0

        import time
        start_time = time.time()
        path = search.aStarSearch(problem, heuristic=hfn)
        elapsed = time.time() - start_time

        if path and len(path) > 0:
            print(f"  Found solution of length {len(path)}.")
            print(f"  Expanded nodes = {problem.expanded_nodes}, "
                  f"max fringe = {problem.max_fringe}, time={elapsed:.3f}s")
        else:
            print("  No solution found.")


if __name__ == "__main__":
    demoTest()
