import pygame
from .base import Hexagon


class GroundHexagon(Hexagon):
    def update(self, t):
        pass

    def draw(self, screen):
        brown = (139, 69, 19)
        pygame.draw.polygon(screen, brown, self.points, 0)
        pygame.draw.polygon(screen, (200, 200, 200), self.points, 1) 