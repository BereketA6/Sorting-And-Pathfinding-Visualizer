class Node:
    """A single cell in the pathfinding grid."""
    __slots__ = ("row", "col", "is_wall", "is_start", "is_end")

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_wall = False
        self.is_start = False
        self.is_end = False


def make_grid(rows, cols):
    return [[Node(r, c) for c in range(cols)] for r in range(rows)]


def reset_search_state(grid):
    """Clears walls/start/end are kept; this only matters for re-running
    a search on the same layout, which the search functions already
    handle by not mutating the grid — kept here for clarity/extension."""
    pass
