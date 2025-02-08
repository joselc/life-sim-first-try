import math
import random
import pygame
from .base import Hexagon
from ..config import COLORS


class PlantHexagon(Hexagon):
    def __init__(self, cx, cy, a):
        super().__init__(cx, cy, a)
        self.phase = random.uniform(0, 2 * math.pi)
        self.t = 0

    def update(self, t):
        self.t = t

    def draw(self, screen):
        green = COLORS['GREEN']
        brown = COLORS['BROWN']
        factor = 0.5 * (1 + math.sin(self.t + self.phase))
        fill_color = (
            int(brown[0] * (1 - factor) + green[0] * factor),
            int(brown[1] * (1 - factor) + green[1] * factor),
            int(brown[2] * (1 - factor) + green[2] * factor)
        )
        pygame.draw.polygon(screen, fill_color, self.points, 0)
        pygame.draw.polygon(screen, COLORS['GRID_LINES'], self.points, 1) 