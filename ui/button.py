import pygame


class Button:
    def __init__(self, rect, text, font, bg_color, text_color, active=False):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.active = active  # visually highlighted, e.g. currently-selected algorithm

    def draw(self, surface, hover_color=None):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)

        color = self.bg_color
        if self.active:
            color = hover_color or self.bg_color
        elif is_hovered:
            color = tuple(min(255, c + 20) for c in self.bg_color)

        pygame.draw.rect(surface, color, self.rect, border_radius=4)
        pygame.draw.rect(surface, (60, 50, 38), self.rect, width=1, border_radius=4)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
