# path_optimizer

This is an interactive framework to test different algorithms used for finding the optimal path between two points in a space where certain points are connected by paths which make traversal easy.

## Requirements:
- python 3.11
- pygame

## Usage

`q` - set start point
`r` - set end point
`w` - lay start of path
`e` - lay end of path
`c` - undo last laid path
`j` - toggle active solution

The solution is implemented in `algorithm.py`, and is computed whenever active solution is enabled with `j`

The current approach requires a complexity of O(n<sup>2</sup>) for preprocessing, where n is the number of paths. The search algorithm used is Dijkstra on a complete graph of (n+2) nodes.
