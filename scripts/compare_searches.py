"""Run the supplied search implementation and save an observed comparison."""
import ast
import contextlib
import csv
import io
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from hidden_path import main

def run(strategy, filename):
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        main(strategy, str(filename))
    output = stream.getvalue()
    expanded = next(s for s in output.splitlines() if s.startswith('Expanded:'))
    path_line = next((s for s in output.splitlines() if s.startswith('Path Found:')), None)
    match = re.search(r'Taking this path will cost: (\d+)', output)
    return output, {'strategy': strategy, 'expanded_nodes': len(re.findall(r'\(\d+, \d+\)', expanded)),
                    'found': path_line is not None,
                    'path_states': len(ast.literal_eval(path_line.split(': ', 1)[1])) if path_line else 0,
                    'cost': int(match.group(1)) if match else ''}

if __name__ == '__main__':
    records = []
    for name in ['simple.txt', 'terrain_portal.txt', 'blocked.txt']:
        for strategy in 'BDUGAH':
            output, row = run(strategy, ROOT / 'examples' / name)
            records.append({'map': name, **row})
            print(name, row)
            target = ROOT / 'results' / f'{Path(name).stem}_{strategy}.txt'
            target.parent.mkdir(exist_ok=True)
            target.write_text(output, encoding='utf-8')
    with (ROOT / 'results/comparison.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
