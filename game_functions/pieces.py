import pygame

class Piece:
    def __init__(self, color, x, y, piece_type):
        self.color = color
        self.x = x
        self.y = y
        self.type = piece_type

    def draw(self, surface, x, y):
        if(x >= 0 ):
            self.x = x
        if(y >= 0):
            self.y = y
        img = pygame.image.load(f"assets/{self.type}_{self.color}.png")
        img.convert()
        rect = img.get_rect(topleft=(self.x, self.y))
        surface.blit(img, rect)