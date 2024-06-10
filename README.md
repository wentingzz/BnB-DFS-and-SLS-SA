# TSP Solver Implementations

This repository contains various implementations of solvers for the Traveling Salesman Problem (TSP). The solutions include:

1. **Branch and Bound with Depth-First Search (BnB_DFS)**
2. **Simulated Annealing with Stochastic Local Search (SLS)**

## Contents

- [BnB_DFS](BnB_DFS): Branch and Bound with Depth-First Search implementation
- [SLS](SLS): Simulated Annealing with Stochastic Local Search implementation

## Branch and Bound with Depth-First Search (BnB_DFS)

The Branch and Bound with Depth-First Search (BnB_DFS) algorithm is a combinatorial optimization method used to solve the Traveling Salesman Problem (TSP). This approach involves systematically exploring the decision tree by dividing it into smaller subproblems (branching) and calculating an estimated lower bound of the minimum cost (bounding). The algorithm employs depth-first search to traverse the tree, backtracking when the current path exceeds the known upper bound, effectively pruning suboptimal solutions. By continuously refining the bounds, BnB_DFS efficiently narrows down the possible solutions, ultimately identifying the optimal route that minimizes the total travel distance or cost.

## Simulated Annealing with Stochastic Local Search (SLS)

Simulated Annealing with Stochastic Local Search (SLS) is a probabilistic technique for approximating the global optimum of a given function, applied here to the Traveling Salesman Problem (TSP). This algorithm mimics the annealing process in metallurgy, where a material is heated and then slowly cooled to decrease defects, thus finding a low-energy state. In SLS, the algorithm starts with an initial solution and explores neighboring solutions by making small changes. It probabilistically decides whether to accept these changes based on a temperature parameter that gradually decreases over time. By allowing uphill moves (worse solutions) with a certain probability, the algorithm avoids getting trapped in local minima and converges towards the global optimum as the temperature lowers.

## Usage

To run the implementations, navigate to the respective directories and follow the instructions in the individual README files.

Required packages:

- numpy
- matplotlib
- time

First, make sure to change `source` in `BnB_DFS.py` or  to the path of your test file before running. If you are running SLS with SA, make sure to change `file` in the main function of `SLS.py` to the path of your test file before running.

For Branch and Bound with Depth-First Search:

```bash
cd BnB_DFS
python .\BnB_DFS.py
```

For Simulated Annealing with Stochastic Local Search:

```bash
cd SLS
python python .\SLS.py
```

## Acknowledgments

- The BnB_DFS implementation is inspired by classical Branch and Bound techniques.
- The SLS implementation follows the principles of Simulated Annealing and Local Search methods.
