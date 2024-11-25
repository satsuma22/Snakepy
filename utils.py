from pygame.rect import Rect
from pygame.surface import Surface
import pygame

class Button(Rect):
    def __init__(self, left, top, width, height, text):
        super().__init__(left, top, width, height)
        self.text = text
        self.background_color = (25, 25, 25)
        self.text_color = (255, 255, 255)

    def draw(self, surface, text_size):
        pygame.draw.rect(surface, self.background_color, self)
        button_text = pygame.font.SysFont("Times New Roman MS", text_size)
        text_surface = button_text.render(self.text, True, self.text_color)
        surface.blit(text_surface, (self.x, self.y))
