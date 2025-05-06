import heapq
import sys
import collections

keys_char = [chr(i) for i in range(ord('a'), ord('z') + 1)]
doors_char = [k.upper() for k in keys_char]


def get_input():
    """Чтение данных из стандартного ввода."""
    return [list(line.strip()) for line in sys.stdin]


def get_edges(grid, start_row, start_col, key_index):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    edges = []
    visited = set()
    queue = collections.deque()
    queue.append((start_row, start_col, 0, 0))
    visited.add((start_row, start_col, 0))
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        row, col, mask, dist = queue.popleft()
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                cell = grid[nr][nc]
                if cell == '#':
                    continue
                new_mask = mask
                if cell in doors_char:
                    door_idx = doors_char.index(cell)
                    new_mask |= (1 << door_idx)

                if cell in key_index:
                    key_pos_in_graph = 4 + key_index[cell]
                    edges.append((key_pos_in_graph, new_mask, dist + 1))
                if (nr, nc, new_mask) not in visited:
                    visited.add((nr, nc, new_mask))
                    queue.append((nr, nc, new_mask, dist + 1))
    return edges


def build_graph(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    points = []
    key_set = set()

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '@':
                points.append((i, j))

    for i in range(rows):
        for j in range(cols):
            c = grid[i][j]
            if c in keys_char:
                key_set.add(c)

    sorted_keys = sorted(key_set)
    key_index = {k: idx for idx, k in enumerate(sorted_keys)}
    key_count = len(sorted_keys)

    for k in sorted_keys:
        found = False
        for i in range(rows):
            if found:
                break
            for j in range(cols):
                if grid[i][j] == k:
                    points.append((i, j))
                    found = True
                    break

    graph = []
    for point in points:
        edges = get_edges(grid, point[0], point[1], key_index)
        graph.append(edges)

    return graph, key_count


def solve(data):
    graph, key_count = build_graph(data)
    if key_count == 0:
        return 0
    all_keys_mask = (1 << key_count) - 1

    initial_pos = (0, 1, 2, 3)
    initial_mask = 0
    initial_state = (*initial_pos, initial_mask)
    heap = []
    heapq.heappush(heap, (0, initial_state))
    min_dist = {initial_state: 0}

    while heap:
        current_dist, current_state = heapq.heappop(heap)
        if min_dist[current_state] < current_dist:
            continue

        pos0, pos1, pos2, pos3, mask = current_state
        if mask == all_keys_mask:
            return current_dist

        for robot_idx in range(4):
            current_pos = [pos0, pos1, pos2, pos3]
            robot_node = current_pos[robot_idx]

            for (next_node, req_mask, add_dist) in graph[robot_node]:
                if (mask & req_mask) != req_mask:
                    continue

                if next_node >= 4:
                    key_bit = 1 << (next_node - 4)
                    if (mask & key_bit) != 0:
                        continue
                    new_mask = mask | key_bit
                else:
                    new_mask = mask

                new_pos = current_pos.copy()
                new_pos[robot_idx] = next_node
                new_state = (
                    new_pos[0], new_pos[1], new_pos[2], new_pos[3], new_mask)
                new_dist = current_dist + add_dist

                if new_state not in min_dist or new_dist < min_dist[new_state]:
                    min_dist[new_state] = new_dist
                    heapq.heappush(heap, (new_dist, new_state))

    return -1


def main():
    data = get_input()
    result = solve(data)
    print(result)


if __name__ == '__main__':
    main()
