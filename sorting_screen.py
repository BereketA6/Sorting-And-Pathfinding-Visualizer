import pygame
import random
import time
from algorithms.sorting import ALGORITHMS
from ui.button import Button

WIDTH, HEIGHT = 900, 600
BG = (15, 12, 9)
PANEL = (23, 19, 14)
BAR_DEFAULT = (150, 130, 100)
BAR_COMPARE = (240, 200, 60)
BAR_SWAP = (229, 86, 74)
BAR_SORTED = (111, 191, 122)
ACCENT = (240, 160, 48)
TEXT = (245, 240, 230)
TEXT_DIM = (150, 138, 122)


class SortingVisualizer:
    def __init__(self, screen, fonts):
        self.screen = screen
        self.font_title = fonts["title"]
        self.font_body = fonts["body"]
        self.font_small = fonts["small"]

        self.array_size = 40
        self.array = self._random_array(self.array_size)
        self.generator = None
        self.current_state = (self.array[:], (), (), set())
        self.running = False
        self.speed = 30  # steps per second
        self.last_step_time = 0
        self.comparisons = 0
        self.swaps = 0
        self.start_time = None
        self.elapsed = 0.0
        self.finished = False

        self.algo_names = list(ALGORITHMS.keys())
        self.selected_algo = self.algo_names[0]

        self._build_buttons()

    def _random_array(self, n):
        return [random.randint(20, 400) for _ in range(n)]

    def _build_buttons(self):
        self.algo_buttons = []
        x = 20
        for name in self.algo_names:
            w = self.font_small.size(name)[0] + 24
            self.algo_buttons.append(Button((x, 20, w, 32), name, self.font_small, PANEL, TEXT))
            x += w + 8

        self.play_button = Button((20, HEIGHT - 50, 90, 34), "Play", self.font_body, ACCENT, (20, 15, 10))
        self.reset_button = Button((120, HEIGHT - 50, 90, 34), "Reset", self.font_body, PANEL, TEXT)
        self.speed_up_button = Button((WIDTH - 140, HEIGHT - 50, 34, 34), "+", self.font_body, PANEL, TEXT)
        self.speed_down_button = Button((WIDTH - 180, HEIGHT - 50, 34, 34), "-", self.font_body, PANEL, TEXT)

    def handle_click(self, pos):
        for btn, name in zip(self.algo_buttons, self.algo_names):
            if btn.is_clicked(pos):
                self.selected_algo = name
                self.reset()
                return

        if self.play_button.is_clicked(pos):
            self.toggle_play()
        elif self.reset_button.is_clicked(pos):
            self.reset()
        elif self.speed_up_button.is_clicked(pos):
            self.speed = min(200, self.speed + 10)
        elif self.speed_down_button.is_clicked(pos):
            self.speed = max(2, self.speed - 10)

    def toggle_play(self):
        if self.finished:
            return
        if self.generator is None:
            self.generator = ALGORITHMS[self.selected_algo](self.array)
            self.start_time = time.time()
        self.running = not self.running

    def reset(self):
        self.array = self._random_array(self.array_size)
        self.generator = None
        self.current_state = (self.array[:], (), (), set())
        self.running = False
        self.comparisons = 0
        self.swaps = 0
        self.start_time = None
        self.elapsed = 0.0
        self.finished = False

    def update(self):
        if not self.running or self.generator is None:
            return

        now = time.time()
        interval = 1.0 / self.speed
        if now - self.last_step_time < interval:
            return
        self.last_step_time = now

        try:
            state = next(self.generator)
            self.current_state = state
            _, comparing, swapped, _ = state
            if comparing:
                self.comparisons += 1
            if swapped:
                self.swaps += 1
            self.elapsed = time.time() - self.start_time
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

        array, comparing, swapped, sorted_idx = self.current_state
        n = len(array)
        chart_top = 80
        chart_bottom = HEIGHT - 100
        chart_height = chart_bottom - chart_top
        bar_width = (WIDTH - 40) / n
        max_val = max(array) if array else 1

        for i, val in enumerate(array):
            bar_h = (val / max_val) * chart_height
            x = 20 + i * bar_width
            y = chart_bottom - bar_h

            if i in sorted_idx:
                color = BAR_SORTED
            elif i in swapped:
                color = BAR_SWAP
            elif i in comparing:
                color = BAR_COMPARE
            else:
                color = BAR_DEFAULT

            pygame.draw.rect(self.screen, color, (x, y, max(bar_width - 1, 1), bar_h))

        stats = f"Comparisons: {self.comparisons}    Swaps: {self.swaps}    Time: {self.elapsed:.2f}s    Speed: {self.speed}"
        stats_surf = self.font_small.render(stats, True, TEXT_DIM)
        self.screen.blit(stats_surf, (20, chart_top - 30))

        if self.finished:
            done_surf = self.font_body.render("Sorted!", True, BAR_SORTED)
            self.screen.blit(done_surf, (WIDTH // 2 - done_surf.get_width() // 2, chart_top - 30))

        self.play_button.text = "Pause" if self.running else ("Play" if not self.finished else "Done")
        self.play_button.draw(self.screen)
        self.reset_button.draw(self.screen)
        self.speed_up_button.draw(self.screen)
        self.speed_down_button.draw(self.screen)

        speed_label = self.font_small.render("Speed", True, TEXT_DIM)
        self.screen.blit(speed_label, (WIDTH - 180, HEIGHT - 74))
