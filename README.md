# Grid search and pathfinding

**Compare six AI search strategies on weighted grids with walls and forced teleport moves.**

A Python command-line project that exposes each algorithm's expansion order, final path
and total movement cost. It makes the difference between finding a short route, finding
a cheap route and following a promising heuristic visible on small reproducible maps.

[中文简介](README.zh-CN.md) · [Search implementation](hidden_path.py) ·
[Example maps](examples/) · [Observed comparisons](results/comparison.csv) · [Tests](tests/test_search.py)

## Features

- BFS with a FIFO queue and DFS with a stack.
- UCS, greedy best-first and A* using heap-based priority queues.
- Strict hill climbing, which can stop at a local minimum or plateau.
- Normal, mud and boulder entry costs of 1, 2 and 3. Walls and grid boundaries block movement.
- Paired portal entrances force a zero-cost transfer to the exit as the next transition.
- Left/right/up/down successor order, coordinate-based priority ties and insertion order
  make the resulting traces deterministic. Already expanded states are discarded.

## A small example

```text
Start: (0, 0)       Goal: X

. B . W 2
M . 1 W X

1 -> 2 is a forced portal transfer with zero extra cost.
Entering either portal tile from an adjacent tile costs 1.
```

| Strategy | Cost on this map | Observation |
|---|---:|---|
| BFS | 6 | Fewest transitions does not guarantee lowest weighted cost |
| DFS | 6 | Follows the specified depth-first expansion order |
| UCS | 5 | Avoids the more expensive boulder route |
| Greedy | 5 | The heuristic happens to guide it to the cheaper route here |
| A* | 5 | Combines accumulated cost and the required heuristic |
| Hill climbing | No path found | Stops when the portal transition would not strictly reduce h |

These are observed results for one demonstration map, not a general performance ranking.
See the saved [expansion traces](results/) and regenerate them with the comparison script.

## Run

Requires Python 3.10+ and the standard library only.

```bash
python hidden_path.py U examples/terrain_portal.txt
python hidden_path.py A examples/simple.txt
python scripts/compare_searches.py
python -m unittest discover -s tests -v
```

Strategy flags: `B` BFS, `D` DFS, `U` UCS, `G` greedy, `A` A*, `H` hill climbing.

Example output for UCS:

```text
UCS Search Initiated
Expanded: (0, 0)(0, 1)(1, 0)(1, 1)(2, 0)(2, 1)(4, 0)(4, 1)
Path Found: [(0, 0), (0, 1), (1, 1), (2, 1), (4, 0), (4, 1)]
Taking this path will cost: 5 Willpower
```

## Map format

The first line is `widthxheight`, the second is `start_x-start_y`, and the remaining
lines are rows of `.`, `W`, `M`, `B`, `X` or portal digits. Coordinates start at the
upper-left corner, with x increasing rightwards and y increasing downwards.

The supplied implementation pairs odd entrances with the following even digit
(`1->2`, `3->4`, `5->6`, `7->8`). It does not implement a `9->0` wraparound pair.
The goal is a single `X` tile. Example files are included, so no external dataset is needed.

## Heuristic and scope

Greedy, A* and hill climbing use Manhattan distance, with a portal entrance assigned
its exit's heuristic. Teleport shortcuts can make ordinary Manhattan distance
overestimate the true remaining cost at other cells. Therefore this preserved A*
implementation, which closes states without reopening, is **not advertised as generally
cost-optimal on arbitrary portal maps**. UCS is the cost-based reference for nonnegative
transition costs. Hill climbing deliberately requires strict improvement, so a portal's
equal-heuristic transition can stop it even when a route exists.

## Project provenance

Originally an individual university AI search exercise. This public edition keeps the
standalone implementation supplied by the author and adds documentation, reproducible
example runs and focused tests. Alternative drafts and the full course handout are not
included. This is a graph-search project, not a machine-learning training pipeline.
