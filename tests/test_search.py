import contextlib
import io
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from hidden_path import main

def output(strategy, name):
    text = io.StringIO()
    with contextlib.redirect_stdout(text):
        main(strategy, str(ROOT / 'examples' / name))
    return text.getvalue()

class SearchChecks(unittest.TestCase):
    def test_simple_success_for_all_strategies(self):
        for strategy in 'BDUGAH':
            with self.subTest(strategy=strategy):
                text = output(strategy, 'simple.txt')
                self.assertIn('Path Found: [(2, 1), (1, 1), (0, 1), (0, 0)]', text)
                self.assertIn('cost: 3 Willpower', text)

    def test_weighted_terrain_changes_the_best_cost(self):
        bfs = output('B', 'terrain_portal.txt')
        ucs = output('U', 'terrain_portal.txt')
        self.assertIn('cost: 6 Willpower', bfs)
        self.assertIn('cost: 5 Willpower', ucs)
        self.assertIn('(2, 1), (4, 0)', ucs)

    def test_priority_expansion_order(self):
        self.assertIn('Expanded: (0, 0)(0, 1)(1, 0)(1, 1)(2, 0)(2, 1)(4, 0)(4, 1)',
                      output('U', 'terrain_portal.txt'))

    def test_hill_climbing_stops_on_portal_plateau(self):
        text = output('H', 'terrain_portal.txt')
        self.assertIn('Expanded: (0, 0)(0, 1)(1, 1)(2, 1)', text)
        self.assertIn('NO PATH FOUND!', text)
        self.assertNotIn('Willpower', text)

    def test_unreachable_goal(self):
        for strategy in 'BDUGAH':
            with self.subTest(strategy=strategy):
                self.assertIn('NO PATH FOUND!', output(strategy, 'blocked.txt'))

    def test_start_is_goal(self):
        for strategy in 'BDUGAH':
            with self.subTest(strategy=strategy):
                self.assertIn('cost: 0 Willpower', output(strategy, 'already_at_goal.txt'))

if __name__ == '__main__':
    unittest.main()
