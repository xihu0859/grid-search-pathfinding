import sys
import heapq
from collections import deque

def main(strategy, filename):
    try:
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        return

    width, height = map(int, lines[0].split('x'))
    start_x, start_y = map(int, lines[1].split('-'))
    start_pos = (start_x, start_y)
    grid = lines[2:]

    treasure_pos = None
    portals = {} 
    portal_temp = {} 
    for y in range(height):
        for x in range(width):
            char = grid[y][x]
            if char == 'X':
                treasure_pos = (x, y)
            elif char.isdigit():
                portal_temp[int(char)] = (x, y)

    for pid, pos in portal_temp.items():
        if pid % 2 != 0 and (pid + 1) in portal_temp:
            portals[pos] = portal_temp[pid + 1]

    def get_manhattan(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def get_h(pos):
        target = portals[pos] if pos in portals else pos
        return get_manhattan(target, treasure_pos)

    def get_successors(pos):
        if pos in portals:
            return [("TELEPORT", portals[pos], 0)]
        
        results = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = pos[0] + dx, pos[1] + dy
            if 0 <= nx < width and 0 <= ny < height:
                char = grid[ny][nx]
                if char != 'W': 
                    cost = 3 if char == 'B' else (2 if char == 'M' else 1)
                    results.append((None, (nx, ny), cost))
        return results

    strategy_names = {'B':'BFS', 'D':'DFS', 'U':'UCS', 'G':'Greedy', 'A':'A*', 'H':'Hill-climbing'}
    print(f"{strategy_names.get(strategy, strategy)} Search Initiated")

    expanded = []
    found_path = None
    found_cost = 0
    closed_set = set() 
    time_counter = 0 

    if strategy == 'B':
        fringe = deque([(start_pos, [start_pos], 0)])
        while fringe:
            curr, path, cost = fringe.popleft()
            if curr in closed_set: continue
            expanded.append(curr)
            closed_set.add(curr)
            if curr == treasure_pos:
                found_path, found_cost = path, cost
                break
            for _, next_pos, step_cost in get_successors(curr):
                if next_pos not in closed_set:
                    fringe.append((next_pos, path + [next_pos], cost + step_cost))

    elif strategy == 'D':
        fringe = [(start_pos, [start_pos], 0)]
        while fringe:
            curr, path, cost = fringe.pop()
            if curr in closed_set: continue
            expanded.append(curr)
            closed_set.add(curr)
            if curr == treasure_pos:
                found_path, found_cost = path, cost
                break
            for _, next_pos, step_cost in reversed(get_successors(curr)):
                if next_pos not in closed_set:
                    fringe.append((next_pos, path + [next_pos], cost + step_cost))

    elif strategy in ['U', 'G', 'A']:
        time_counter += 1
        start_h = get_h(start_pos)
        prio = 0 if strategy == 'U' else start_h
        fringe = [((prio, start_pos[0], start_pos[1], time_counter), start_pos, [start_pos], 0)]
        while fringe:
            (p, x, y, t), curr, path, cost = heapq.heappop(fringe)
            if curr in closed_set: continue
            expanded.append(curr)
            closed_set.add(curr)
            if curr == treasure_pos:
                found_path, found_cost = path, cost
                break
            for _, next_pos, step_cost in get_successors(curr):
                if next_pos not in closed_set:
                    time_counter += 1
                    g_n = cost + step_cost
                    h_n = get_h(next_pos)
                    if strategy == 'U': p_n = g_n
                    elif strategy == 'G': p_n = h_n
                    else: p_n = g_n + h_n 
                    heapq.heappush(fringe, ((p_n, next_pos[0], next_pos[1], time_counter), next_pos, path + [next_pos], g_n))

    elif strategy == 'H':
        curr, path, cost = start_pos, [start_pos], 0
        while True:
            expanded.append(curr)
            if curr == treasure_pos:
                found_path, found_cost = path, cost
                break
            neighbors = get_successors(curr)
            if not neighbors: break
            best = None
            for _, next_pos, step_cost in neighbors:
                h_n = get_h(next_pos)
                if best is None or h_n < best[0] or (h_n == best[0] and (next_pos[0] < best[1][0] or (next_pos[0] == best[1][0] and next_pos[1] < best[1][1]))):
                    best = (h_n, next_pos, step_cost)
            if best and best[0] < get_h(curr):
                curr, cost = best[1], cost + best[2]
                path.append(curr)
            else: break

    exp_output = "".join([f"({p[0]}, {p[1]})" for p in expanded])
    print(f"Expanded: {exp_output}")
    
    if found_path:
        path_output = ", ".join([f"({p[0]}, {p[1]})" for p in found_path])
        print(f"Path Found: [{path_output}]")
        print(f"Taking this path will cost: {found_cost} Willpower")
    else:
        print("NO PATH FOUND!")

if __name__ == '__main__':   
    if len(sys.argv) < 3:
        strategy = 'B'
        filename = 'example1.txt'
    else:
        strategy = sys.argv[1]
        filename = sys.argv[2]
    main(strategy, filename)
