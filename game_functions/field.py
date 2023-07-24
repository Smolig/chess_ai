import pygame

class Field:
    def __init__(self, x, y, fig):
        self.x = x
        self.y = y
        self.fig = fig

    def draw(self,surface):
        pygame.draw.rect(surface, (96,165,165), (self.x, self.y, 75, 75))