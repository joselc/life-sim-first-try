import pygame
from .base import Hexagon
from ..config import COLORS


class GroundHexagon(Hexagon):
    def update(self, t):
        pass

    def draw(self, screen):
        pygame.draw.polygon(screen, COLORS['BROWN'], self.points, 0)
        pygame.draw.polygon(screen, COLORS['GRID_LINES'], self.points, 1) 