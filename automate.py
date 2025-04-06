#!/usr/bin/env python3
"""
automate.py

This file handles:
1) Sprint #3: Generating many 15-puzzle scenarios (or reading them from scenarios.csv),
   running each puzzle with A* using each of the four heuristics (h1..h4),
   and recording metrics (solution depth, expanded nodes, fringe size, execution time).
   Aggregated averages are then printed.

We mark changes with the required special comment blocks.
"""

import csv
import time
import search
from fifteenpuzzle import (
    FifteenPuzzleState,
    FifteenPuzzleSearchProblem,
    createRandomFifteenPuzzle,
    h1_misplacedTiles,
    h2_euclideanDistance,
    h3_manhattanDistance,
    h4_rowColDifference
)

##############################
# /*=====Start Change Task 3=====*/
##############################
def generateScenariosCSV(filename="scenarios.csv", count=10, shuffle=20):
    """
    (Sprint #3)
    Generate 'count' random 15-puzzle states by shuffling the goal state 'shuffle' times,
    then write each state as 16 comma-separated numbers to a CSV file.

    Increase 'shuffle' to produce more difficult puzzles, but it may take longer to solve.
    """
    import random
    with open(filename, "w", newline="") as fout:
        writer = csv.writer(fout)
        for _ in range(count):
            puzzle = createRandomFifteenPuzzle(shuffle)
            flat = [cell for row in puzzle.cells for cell in row]
            writer.writerow(flat)

def runHeuristicsOnScenarios(filename="scenarios.csv"):
    """
    (Sprint #3)
    Reads each puzzle scenario from 'filename'. For each scenario, runs A* with each of
    the four heuristics, and records:
      - The solution depth (length of the path),
      - The number of nodes expanded,
      - The maximum fringe size, and
      - The execution time.
    Aggregates results and prints a summary table.

    Because all heuristics are admissible, solution depth will be the same for each puzzle.
    The differences show up in expansions, fringe, or time.
    """
    heuristics = [
        (h1_misplacedTiles, "Misplaced Tiles"),
        (h2_euclideanDistance, "Euclidean Distance"),
        (h3_manhattanDistance, "Manhattan Distance"),
        (h4_rowColDifference, "Row/Col Difference")
    ]
    
    stats = {name: {"count": 0, "sumDepth": 0, "sumTime": 0.0, 
                    "sumExp": 0, "sumFringe": 0} for (_, name) in heuristics}
    
    with open(filename, "r") as fin:
        reader = csv.reader(fin)
        scenario_num = 0
        for row in reader:
            scenario_num += 1
            tiles = [int(x) for x in row]
            puzzleState = FifteenPuzzleState(tiles)
            
            print(f"\nScenario #{scenario_num}, puzzle:")
            print(puzzleState)
            
            for (heur_fn, heur_name) in heuristics:
                problem = FifteenPuzzleSearchProblem(puzzleState)
                
                start_time = time.time()
                path = search.aStarSearch(problem, heuristic=heur_fn)
                elapsed = time.time() - start_time
                
                if path is None or len(path) == 0:
                    print(f"  {heur_name}: No solution found or zero moves.")
                else:
                    depth = len(path)
                    expanded = problem.expanded_nodes
                    fringe = problem.max_fringe
                    print(f"  {heur_name}: depth={depth}, expansions={expanded}, fringe={fringe}, time={elapsed:.3f}s")
                    
                    # Accumulate stats
                    stats[heur_name]["count"] += 1
                    stats[heur_name]["sumDepth"] += depth
                    stats[heur_name]["sumTime"] += elapsed
                    stats[heur_name]["sumExp"] += expanded
                    stats[heur_name]["sumFringe"] += fringe

    print("\n=== Sprint #3: Aggregated Heuristic Results ===")
    for (_, heur_name) in heuristics:
        c = stats[heur_name]["count"]
        if c == 0:
            print(f" {heur_name}: No solutions found.")
        else:
            avg_depth = stats[heur_name]["sumDepth"] / c
            avg_time = stats[heur_name]["sumTime"] / c
            avg_exp = stats[heur_name]["sumExp"] / c
            avg_fringe = stats[heur_name]["sumFringe"] / c
            print(f" {heur_name}: #Solved={c}, avgDepth={avg_depth:.2f}, avgTime={avg_time:.3f}s, avgExp={avg_exp:.1f}, avgFringe={avg_fringe:.1f}")
##############################
# /*=====End Change Task 3=====*/
##############################

if __name__ == "__main__":
    # Generate puzzle scenarios (somewhat challenging)
    generateScenariosCSV("scenarios.csv", count=20, shuffle=50)
    
    # Run A* with each heuristic on all scenarios and print aggregated results
    runHeuristicsOnScenarios("scenarios.csv")
