import math
from typing import List, Tuple
import pygame


class Hexagon:
    def __init__(self, cx: float, cy: float, a: float) -> None:
        self.cx = cx
        self.cy = cy
        self.a = a
        self.points: List[Tuple[float, float]] = [
            (cx + a, cy),
            (cx + a/2, cy + (a * math.sqrt(3) / 2)),
            (cx - a/2, cy + (a * math.sqrt(3) / 2)),
            (cx - a, cy),
            (cx - a/2, cy - (a * math.sqrt(3) / 2)),
            (cx + a/2, cy - (a * math.sqrt(3) / 2))
        ]
    
    def update(self, t: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        pass 