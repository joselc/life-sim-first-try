import math
import pygame


class Hexagon:
    def __init__(self, cx, cy, a):
        self.cx = cx
        self.cy = cy
        self.a = a
        self.points = [
            (cx + a, cy),
            (cx + a/2, cy + (a * math.sqrt(3) / 2)),
            (cx - a/2, cy + (a * math.sqrt(3) / 2)),
            (cx - a, cy),
            (cx - a/2, cy - (a * math.sqrt(3) / 2)),
            (cx + a/2, cy - (a * math.sqrt(3) / 2))
        ]
    
    def update(self, t):
        pass

    def draw(self, screen):
        pass 