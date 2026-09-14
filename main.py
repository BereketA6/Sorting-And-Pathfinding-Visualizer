import pygame
import sys
from sorting_screen import SortingVisualizer
from pathfinding_screen import PathfindingVisualizer
from ui.button import Button

WIDTH, HEIGHT = 900, 600
BG = (15, 12, 9)
PANEL = (23, 19, 14)
ACCENT = (240, 160, 48)
TEXT = (245, 240, 230)
TEXT_DIM = (150, 138, 122)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Algorithm Visualizer")
clock = pygame.time.Clock()

fonts = {
    "title": pygame.font.SysFont("arial", 32, bold=True),
    "body": pygame.font.SysFont("arial", 16, bold=True),
    "small": pygame.font.SysFont("arial", 13, bold=True),
}


class MenuScreen:
    def __init__(self):
        self.sorting_btn = Button((WIDTH // 2 - 170, 280, 340, 60), "Sorting Visualizer", fonts["body"], PANEL, TEXT)
        self.pathfinding_btn = Button((WIDTH // 2 - 170, 360, 340, 60), "Pathfinding Visualizer", fonts["body"], PANEL, TEXT)

    def draw(self):
        screen.fill(BG)
        title = fonts["title"].render("ALGORITHM VISUALIZER", True, ACCENT)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 160)))
        sub = fonts["small"].render("Pick a mode to explore", True, TEXT_DIM)
        screen.blit(sub, sub.get_rect(center=(WIDTH // 2, 200)))

        self.sorting_btn.draw(screen, hover_color=ACCENT)
        self.pathfinding_btn.draw(screen, hover_color=ACCENT)

    def handle_click(self, pos):
        if self.sorting_btn.is_clicked(pos):
            return "sorting"
        if self.pathfinding_btn.is_clicked(pos):
            return "pathfinding"
        return None


def main():
    state = "menu"
    menu = MenuScreen()
    sorting_viz = None
    pathfinding_viz = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "menu"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if state == "menu":
                    result = menu.handle_click(event.pos)
                    if result == "sorting":
                        sorting_viz = SortingVisualizer(screen, fonts)
                        state = "sorting"
                    elif result == "pathfinding":
                        pathfinding_viz = PathfindingVisualizer(screen, fonts)
                        state = "pathfinding"
                elif state == "sorting":
                    sorting_viz.handle_click(event.pos)
                elif state == "pathfinding":
                    pathfinding_viz.handle_click(event.pos)
                    pathfinding_viz.handle_mouse_down(event.pos, event.button)

            elif event.type == pygame.MOUSEBUTTONUP:
                if state == "pathfinding":
                    pathfinding_viz.handle_mouse_up()

            elif event.type == pygame.MOUSEMOTION:
                if state == "pathfinding":
                    pathfinding_viz.handle_mouse_motion(event.pos)

        if state == "menu":
            menu.draw()
        elif state == "sorting":
            sorting_viz.update()
            sorting_viz.draw()
            back_hint = fonts["small"].render("ESC: back to menu", True, TEXT_DIM)
            screen.blit(back_hint, (WIDTH - 150, 28))
        elif state == "pathfinding":
            pathfinding_viz.update()
            pathfinding_viz.draw()
            back_hint = fonts["small"].render("ESC: back to menu", True, TEXT_DIM)
            screen.blit(back_hint, (WIDTH - 150, 28))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
