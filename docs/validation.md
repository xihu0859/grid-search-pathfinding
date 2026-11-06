# Validation

Checked on 6 November 2026 with Python 3.13.7, using the standard library only.

Six focused unit tests passed, covering all six strategies on a simple map, the weighted
terrain/portal cost difference, deterministic priority expansion order, hill-climbing failure
on a plateau, an unreachable goal, and a start position already at the goal.

The comparison runner generated 18 traces across three example maps. It records expansion
counts, success/failure, path length in states and movement cost in `results/comparison.csv`.
The source implementation supplied by the author was preserved.

These tests are targeted behaviour checks, not a proof of correctness for all inputs or of
cost optimality under the portal heuristic. Known heuristic and portal-pair limitations are
documented in the README rather than hidden behind the successful example results.
