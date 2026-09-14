"""
Headless test: drives the actual app logic (not a reimplementation) and
saves screenshots at key moments, so I can visually verify the real
rendering code works before handing this off.
"""
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

fonts = {
    "title": pygame.font.SysFont("arial", 32, bold=True),
    "body": pygame.font.SysFont("arial", 16, bold=True),
    "small": pygame.font.SysFont("arial", 13, bold=True),
}

from sorting_screen import SortingVisualizer
from pathfinding_screen import PathfindingVisualizer

# --- Test 1: Menu screen ---
import main as main_module
menu = main_module.MenuScreen()
menu.draw()
pygame.image.save(screen, "/tmp/shot_1_menu.png")
print("Saved menu screenshot")

# --- Test 2: Sorting visualizer mid-run ---
sv = SortingVisualizer(screen, fonts)
sv.selected_algo = "Quick Sort"
sv.generator = None
sv.toggle_play()
for _ in range(150):
    sv.last_step_time = 0  # force step every iteration regardless of real time
    sv.update()
sv.draw()
pygame.image.save(screen, "/tmp/shot_2_sorting_mid.png")
print(f"Saved sorting mid-run screenshot (comparisons={sv.comparisons}, swaps={sv.swaps})")

# --- Test 3: Sorting visualizer finished ---
while not sv.finished:
    sv.last_step_time = 0
    sv.update()
sv.draw()
pygame.image.save(screen, "/tmp/shot_3_sorting_done.png")
is_sorted = sv.current_state[0] == sorted(sv.array)
print(f"Sorting finished. Array actually sorted correctly: {is_sorted}")

# --- Test 4: Pathfinding visualizer with some walls, mid-run ---
pv = PathfindingVisualizer(screen, fonts)
pv.selected_algo = "A*"
# Add a wall barrier with a gap, to make sure pathfinding actually routes around it
for r in range(0, 15):
    pv._apply_cell_edit((r, 15))
pv.toggle_play()
for _ in range(60):
    pv.last_step_time = 0
    pv.update()
pv.draw()
pygame.image.save(screen, "/tmp/shot_4_pathfinding_mid.png")
print(f"Saved pathfinding mid-run screenshot (steps={pv.steps_taken}, visited={len(pv.visited)})")

# --- Test 5: Pathfinding finished, verify path found and avoids walls ---
while not pv.finished:
    pv.last_step_time = 0
    pv.update()
pv.draw()
pygame.image.save(screen, "/tmp/shot_5_pathfinding_done.png")
path_avoids_walls = all(not pv.grid[r][c].is_wall for r, c in pv.path)
print(f"Pathfinding finished. Path length: {len(pv.path)}. Path avoids all walls: {path_avoids_walls}")

# --- Test 6: Verify all 5 sorting algorithms produce correctly sorted output ---
from algorithms.sorting import ALGORITHMS as SORT_ALGOS
import random
test_array = [random.randint(1, 1000) for _ in range(60)]
expected = sorted(test_array)
print("\n--- Sorting algorithm correctness check ---")
for name, algo_fn in SORT_ALGOS.items():
    gen = algo_fn(test_array)
    final_state = None
    for state in gen:
        final_state = state
    result_array = final_state[0]
    correct = result_array == expected
    print(f"{name}: {'PASS' if correct else 'FAIL'}")

# --- Test 7: Verify all 4 pathfinding algorithms find a valid path ---
from algorithms.pathfinding import ALGORITHMS as PATH_ALGOS
from algorithms.grid import make_grid

print("\n--- Pathfinding algorithm correctness check ---")
for name, algo_fn in PATH_ALGOS.items():
    grid = make_grid(15, 15)
    # Wall off a line with one gap, forcing the algorithm to route through it
    for r in range(15):
        if r != 7:
            grid[r][7].is_wall = True
    start, end = (0, 0), (14, 14)
    gen = algo_fn(grid, start, end)
    final = None
    for step in gen:
        final = step
    _, _, done, path = final
    valid = path is not None and len(path) > 0 and all(not grid[r][c].is_wall for r, c in path)
    # Confirm path actually passes through the gap
    passes_gap = any(cell == (7, 7) for cell in path) if path else False
    print(f"{name}: path_found={bool(path)}, avoids_walls={valid}, routes_through_gap={passes_gap}, length={len(path) if path else 0}")

print("\nAll tests complete.")
