import pygame
import time
from algorithms.pathfinding import ALGORITHMS
from algorithms.grid import make_grid
from ui.button import Button

WIDTH, HEIGHT = 900, 600
BG = (15, 12, 9)
PANEL = (23, 19, 14)
GRID_LINE = (45, 38, 28)
CELL_DEFAULT = (23, 19, 14)
CELL_WALL = (60, 50, 38)
CELL_START = (111, 191, 122)
CELL_END = (229, 86, 74)
CELL_VISITED = (150, 110, 40)
CELL_FRONTIER = (240, 200, 60)
CELL_PATH = (240, 160, 48)
ACCENT = (240, 160, 48)
TEXT = (245, 240, 230)
TEXT_DIM = (150, 138, 122)

GRID_ROWS, GRID_COLS = 20, 30
GRID_TOP = 80
CELL_SIZE = 18


class PathfindingVisualizer:
    def __init__(self, screen, fonts):
        self.screen = screen
        self.font_body = fonts["body"]
        self.font_small = fonts["small"]

        self.grid = make_grid(GRID_ROWS, GRID_COLS)
        self.start = (2, 2)
        self.end = (GRID_ROWS - 3, GRID_COLS - 3)
        self.grid[self.start[0]][self.start[1]].is_start = True
        self.grid[self.end[0]][self.end[1]].is_end = True

        self.algo_names = list(ALGORITHMS.keys())
        self.selected_algo = self.algo_names[0]

        self.generator = None
        self.visited = set()
        self.frontier = set()
        self.path = []
        self.running = False
        self.finished = False
        self.speed = 60
        self.last_step_time = 0
        self.steps_taken = 0
        self.start_time = None
        self.elapsed = 0.0

        self.mode = "wall"  # "wall" | "start" | "end"
        self.mouse_down = False
        self.erase_mode = False

        self._build_buttons()

    def _build_buttons(self):
        self.algo_buttons = []
        x = 20
        for name in self.algo_names:
            w = self.font_small.size(name)[0] + 24
            self.algo_buttons.append(Button((x, 20, w, 32), name, self.font_small, PANEL, TEXT))
            x += w + 8

        self.play_button = Button((20, HEIGHT - 50, 90, 34), "Play", self.font_body, ACCENT, (20, 15, 10))
        self.reset_button = Button((120, HEIGHT - 50, 110, 34), "Clear Walls", self.font_body, PANEL, TEXT)
        self.set_start_button = Button((250, HEIGHT - 50, 90, 34), "Set Start", self.font_small, PANEL, TEXT)
        self.set_end_button = Button((350, HEIGHT - 50, 80, 34), "Set End", self.font_small, PANEL, TEXT)

    def _cell_at_pixel(self, pos):
        x, y = pos
        if y < GRID_TOP:
            return None
        col = (x - self._grid_x_offset()) // CELL_SIZE
        row = (y - GRID_TOP) // CELL_SIZE
        if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS:
            return int(row), int(col)
        return None

    def _grid_x_offset(self):
        return (WIDTH - GRID_COLS * CELL_SIZE) // 2

    def handle_click(self, pos):
        for btn, name in zip(self.algo_buttons, self.algo_names):
            if btn.is_clicked(pos):
                self.selected_algo = name
                self.reset_search()
                return

        if self.play_button.is_clicked(pos):
            self.toggle_play()
            return
        if self.reset_button.is_clicked(pos):
            self.clear_walls()
            return
        if self.set_start_button.is_clicked(pos):
            self.mode = "start"
            return
        if self.set_end_button.is_clicked(pos):
            self.mode = "end"
            return

        cell = self._cell_at_pixel(pos)
        if cell:
            self._apply_cell_edit(cell)

    def handle_mouse_down(self, pos, button):
        self.mouse_down = True
        self.erase_mode = (button == 3)  # right-click erases walls
        cell = self._cell_at_pixel(pos)
        if cell and self.mode == "wall":
            self._apply_cell_edit(cell)

    def handle_mouse_up(self):
        self.mouse_down = False

    def handle_mouse_motion(self, pos):
        if self.mouse_down and self.mode == "wall":
            cell = self._cell_at_pixel(pos)
            if cell:
                self._apply_cell_edit(cell)

    def _apply_cell_edit(self, cell):
        row, col = cell
        node = self.grid[row][col]

        if self.mode == "start":
            if not node.is_wall and cell != self.end:
                self.grid[self.start[0]][self.start[1]].is_start = False
                self.start = cell
                node.is_start = True
            self.mode = "wall"
        elif self.mode == "end":
            if not node.is_wall and cell != self.start:
                self.grid[self.end[0]][self.end[1]].is_end = False
                self.end = cell
                node.is_end = True
            self.mode = "wall"
        else:
            if cell != self.start and cell != self.end:
                node.is_wall = not self.erase_mode

    def clear_walls(self):
        for row in self.grid:
            for node in row:
                node.is_wall = False
        self.reset_search()

    def reset_search(self):
        self.generator = None
        self.visited = set()
        self.frontier = set()
        self.path = []
        self.running = False
        self.finished = False
        self.steps_taken = 0
        self.start_time = None
        self.elapsed = 0.0

    def toggle_play(self):
        if self.finished:
            self.reset_search()
        if self.generator is None:
            self.generator = ALGORITHMS[self.selected_algo](self.grid, self.start, self.end)
            self.start_time = time.time()
        self.running = not self.running

    def update(self):
        if not self.running or self.generator is None:
            return

        now = time.time()
        interval = 1.0 / self.speed
        if now - self.last_step_time < interval:
            return
        self.last_step_time = now

        try:
            visited_step, frontier_snapshot, done, path = next(self.generator)
            self.visited |= visited_step
            self.frontier = frontier_snapshot
            self.steps_taken += 1
            self.elapsed = time.time() - self.start_time
            if done:
                self.path = path or []
                self.running = False
                self.finished = True
        except StopIteration:
            self.running = False
            self.finished = True

    def draw(self):
        self.screen.fill(BG)

        for btn, name in zip(self.algo_buttons, self.algo_names):
            btn.active = (name == self.selected_algo)
            btn.draw(self.screen, hover_color=ACCENT)
            if btn.active:
                text_surf = self.font_small.render(name, True, (20, 15, 10))
                self.screen.blit(text_surf, text_surf.get_rect(center=btn.rect.center))

        x_offset = self._grid_x_offset()
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                node = self.grid[row][col]
                x = x_offset + col * CELL_SIZE
                y = GRID_TOP + row * CELL_SIZE
                cell = (row, col)

                if node.is_start:
                    color = CELL_START
                elif node.is_end:
                    color = CELL_END
                elif node.is_wall:
                    color = CELL_WALL
                elif cell in self.path:
                    color = CELL_PATH
                elif cell in self.visited:
                    color = CELL_VISITED
                elif cell in self.frontier:
                    color = CELL_FRONTIER
                else:
                    color = CELL_DEFAULT

                pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE - 1, CELL_SIZE - 1))

        grid_pixel_h = GRID_ROWS * CELL_SIZE
        pygame.draw.rect(self.screen, GRID_LINE, (x_offset, GRID_TOP, GRID_COLS * CELL_SIZE, grid_pixel_h), width=1)

        stats = f"Steps: {self.steps_taken}    Visited: {len(self.visited)}    Time: {self.elapsed:.2f}s"
        if self.finished:
            stats += f"    Path length: {len(self.path)}" if self.path else "    No path found"
        stats_surf = self.font_small.render(stats, True, TEXT_DIM)
        self.screen.blit(stats_surf, (20, GRID_TOP - 30))

        hint = self.font_small.render("Left-click/drag: draw walls   Right-click/drag: erase", True, TEXT_DIM)
        self.screen.blit(hint, (20, GRID_TOP + grid_pixel_h + 8))

        self.play_button.text = "Pause" if self.running else ("Play" if not self.finished else "Replay")
        self.play_button.draw(self.screen)
        self.reset_button.draw(self.screen)
        self.set_start_button.active = (self.mode == "start")
        self.set_end_button.active = (self.mode == "end")
        self.set_start_button.draw(self.screen, hover_color=CELL_START)
        self.set_end_button.draw(self.screen, hover_color=CELL_END)
