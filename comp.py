#!/usr/bin/env python3
"""
comp.py

Sprint #4: Overall comparison between search strategies.
This file reads puzzle scenarios from scenarios.csv, and for each scenario,
it runs:
   - Breadth-First Search (BFS)
   - Depth-First Search (DFS)
   - Uniform-Cost Search (UCS)
   - A* search using your best heuristic (here assumed to be h3_manhattanDistance)
It collects and aggregates performance metrics (solution depth, expanded nodes, fringe size, execution time)
and then prints the results.
"""

import csv
import time
import search
from fifteenpuzzle import (
    FifteenPuzzleState,
    FifteenPuzzleSearchProblem,
    createRandomFifteenPuzzle,
    h3_manhattanDistance  # Assuming Manhattan is the best heuristic
)

def compareSearchStrategies(filename="scenarios.csv"):
    """
    (Sprint #4)
    Reads puzzle scenarios from 'filename' and compares the following search strategies:
        - BFS, DFS, UCS, and A* (with the Manhattan heuristic).
    For each strategy, it records:
        - Solution depth,
        - Number of expanded nodes,
        - Maximum fringe size,
        - Execution time.
    Aggregated results are printed at the end.
    """
    from search import bfs, dfs, ucs, astar

    # Define A* with the best heuristic as a lambda
    def astar_best(problem):
        return astar(problem, heuristic=h3_manhattanDistance)

    strategies = [
        (bfs, "BFS"),
        (dfs, "DFS"),
        (ucs, "UCS"),
        (astar_best, "A* (Manhattan)")
    ]
    
    # Aggregator for overall stats
    stats = {name: {"count": 0, "sumDepth": 0, "sumTime": 0.0, "sumExp": 0, "sumFringe": 0}
             for (_, name) in strategies}
    
    with open(filename, "r") as fin:
        reader = csv.reader(fin)
        scenario_num = 0
        for row in reader:
            scenario_num += 1
            tiles = [int(x) for x in row]
            puzzleState = FifteenPuzzleState(tiles)
            
            print(f"\nScenario #{scenario_num}, puzzle:")
            print(puzzleState)
            
            for (strategy_fn, strategy_name) in strategies:
                problem = FifteenPuzzleSearchProblem(puzzleState)
                start_time = time.time()
                path = strategy_fn(problem)
                elapsed = time.time() - start_time
                
                if path is None or len(path) == 0:
                    print(f"  {strategy_name}: No solution found or zero moves.")
                else:
                    depth = len(path)
                    expanded = problem.expanded_nodes
                    fringe = problem.max_fringe
                    print(f"  {strategy_name}: depth={depth}, expansions={expanded}, fringe={fringe}, time={elapsed:.3f}s")
                    
                    stats[strategy_name]["count"] += 1
                    stats[strategy_name]["sumDepth"] += depth
                    stats[strategy_name]["sumTime"] += elapsed
                    stats[strategy_name]["sumExp"] += expanded
                    stats[strategy_name]["sumFringe"] += fringe
    
    # Print aggregated results
    print("\n=== Sprint #4: Aggregated Search Strategy Results ===")
    for (_, name) in strategies:
        count = stats[name]["count"]
        if count == 0:
            print(f" {name}: No solutions found.")
        else:
            avg_depth = stats[name]["sumDepth"] / count
            avg_time = stats[name]["sumTime"] / count
            avg_exp = stats[name]["sumExp"] / count
            avg_fringe = stats[name]["sumFringe"] / count
            print(f" {name}: #Solved={count}, avgDepth={avg_depth:.2f}, avgTime={avg_time:.3f}s, avgExp={avg_exp:.1f}, avgFringe={avg_fringe:.1f}")

def main():
    compareSearchStrategies("scenarios.csv")

if __name__ == "__main__":
    main()
