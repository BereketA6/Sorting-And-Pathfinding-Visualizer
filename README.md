# Algorithm Visualizer

An interactive Python/Pygame app that animates sorting and pathfinding
algorithms step-by-step — built to reinforce and demonstrate concepts from
Advanced Data Structures & Algorithms.


## What it does

**Sorting Visualizer** — Bubble, Selection, Insertion, Merge, and Quick sort,
animated as bars. Yellow = comparing, red = swapping, green = confirmed
sorted. Live comparison/swap counters and a speed control.

**Pathfinding Visualizer** — BFS, DFS, Dijkstra, and A*, animated on an
interactive grid. Draw walls with left-click/drag, erase with right-click/drag,
reposition the start/end points, and watch each algorithm search differently
— BFS/Dijkstra expand outward evenly, A* is visibly biased toward the goal,
DFS commits to one direction before backtracking.

## How to run it

```bash
pip install pygame
python3 main.py
```

No database, no API keys, no build step — just Python and Pygame.

## Controls

**Sorting screen:**
- Click an algorithm name to select it (auto-resets)
- Play/Pause to run or pause the animation
- Reset to shuffle a new random array
- +/- to change animation speed
- ESC to return to the menu

**Pathfinding screen:**
- Left-click or drag to draw walls
- Right-click or drag to erase walls
- "Set Start" / "Set End" then click a cell to move the start/end points
- Play/Pause to run the selected algorithm
- "Clear Walls" to reset the grid
- ESC to return to the menu

## Project structure

```
algo-visualizer/
├── main.py                      <- entry point, menu screen, event loop
├── sorting_screen.py             <- sorting visualizer UI + animation driver
├── pathfinding_screen.py         <- pathfinding visualizer UI + animation driver
├── test_headless.py              <- correctness tests (run this to verify everything works)
├── algorithms/
│   ├── sorting.py                <- Bubble/Selection/Insertion/Merge/Quick sort as generators
│   ├── pathfinding.py            <- BFS/DFS/Dijkstra/A* as generators
│   └── grid.py                   <- Node/grid data structure for pathfinding
└── ui/
    └── button.py                 <- reusable clickable button widget
```

## The core design idea

Every algorithm is written as a **Python generator** that `yield`s its
internal state after every meaningful step, instead of computing a final
result and returning it. The visualizer's main loop pulls one step at a
time on a timer and redraws.

This means the sorting/pathfinding code has **zero knowledge that it's
being animated** — `bubble_sort()` doesn't know about Pygame, colors, or
timing. That separation (algorithm logic vs. rendering/animation) is a
real software design principle: it's why you can, for example, plug in a
6th sorting algorithm without touching a single line of drawing code.

## Complexity notes

- **Sorting:** O(n²) algorithms (Bubble, Selection, Insertion) visibly take
  many more steps than O(n log n) algorithms (Merge, Quick) on the same
  array size — you can literally watch the difference by comparing the
  step counters.
- **Pathfinding:** BFS and Dijkstra produce identical results on an
  unweighted grid (Dijkstra visibly "wastes" a priority queue on equal-weight
  edges — worth explaining why Dijkstra generalizes BFS). A* consistently
  visits fewer cells than BFS/Dijkstra because its heuristic biases the
  search toward the goal instead of expanding evenly in all directions.

