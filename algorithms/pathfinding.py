"""
Grid-based pathfinding algorithms, each a generator yielding animation
steps: (visited_this_step, frontier_snapshot, done, path_or_None).

The grid is a 2D list of Node objects (see grid.py). All four algorithms
share the same interface so the visualizer doesn't need algorithm-specific
code to drive the animation.
"""

import heapq
from collections import deque


def _reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path


def _neighbors(node, grid):
    row, col = node
    rows, cols = len(grid), len(grid[0])
    candidates = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
    return [
        (r, c) for r, c in candidates
        if 0 <= r < rows and 0 <= c < cols and not grid[r][c].is_wall
    ]


def bfs(grid, start, end):
    queue = deque([start])
    came_from = {}
    visited = {start}

    while queue:
        current = queue.popleft()
        if current == end:
            yield {current}, set(queue), True, _reconstruct_path(came_from, current)
            return

        for neighbor in _neighbors(current, grid):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)

        yield {current}, set(queue), False, None

    yield set(), set(), True, None  # no path found


def dfs(grid, start, end):
    stack = [start]
    came_from = {}
    visited = {start}

    while stack:
        current = stack.pop()
        if current == end:
            yield {current}, set(stack), True, _reconstruct_path(came_from, current)
            return

        for neighbor in _neighbors(current, grid):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)

        yield {current}, set(stack), False, None

    yield set(), set(), True, None


def dijkstra(grid, start, end):
    # All edges have equal weight (1) since this is a grid, but the
    # priority-queue-based structure is exactly what a weighted version
    # would use — a good talking point on how Dijkstra generalizes BFS.
    pq = [(0, start)]
    came_from = {}
    dist = {start: 0}
    visited = set()

    while pq:
        d, current = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)

        if current == end:
            yield {current}, {n for _, n in pq}, True, _reconstruct_path(came_from, current)
            return

        for neighbor in _neighbors(current, grid):
            new_dist = d + 1
            if neighbor not in dist or new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                came_from[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))

        yield {current}, {n for _, n in pq}, False, None

    yield set(), set(), True, None


def _heuristic(a, b):
    # Manhattan distance — admissible for a grid with only 4-directional movement
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(grid, start, end):
    pq = [(_heuristic(start, end), 0, start)]
    came_from = {}
    g_score = {start: 0}
    visited = set()

    while pq:
        _, d, current = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)

        if current == end:
            yield {current}, {n for _, _, n in pq}, True, _reconstruct_path(came_from, current)
            return

        for neighbor in _neighbors(current, grid):
            tentative_g = d + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                came_from[neighbor] = current
                f_score = tentative_g + _heuristic(neighbor, end)
                heapq.heappush(pq, (f_score, tentative_g, neighbor))

        yield {current}, {n for _, _, n in pq}, False, None

    yield set(), set(), True, None


ALGORITHMS = {
    "BFS": bfs,
    "DFS": dfs,
    "Dijkstra": dijkstra,
    "A*": a_star,
}
