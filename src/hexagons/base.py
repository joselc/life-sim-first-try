import math
from typing import List, Tuple
import pygame


class Hexagon:
    """Base class for hexagonal cells in the life simulation.

    This class provides the basic structure and interface for hexagonal cells,
    including their geometric properties and basic rendering capabilities.

    Attributes:
        cx (float): X-coordinate of the hexagon's center
        cy (float): Y-coordinate of the hexagon's center
        a (float): Length of the hexagon's side
        points (List[Tuple[float, float]]): List of (x, y) coordinates for the hexagon's vertices
    """

    def __init__(self, cx: float, cy: float, a: float) -> None:
        """Initialize a hexagonal cell.

        Args:
            cx (float): X-coordinate of the hexagon's center
            cy (float): Y-coordinate of the hexagon's center
            a (float): Length of the hexagon's side
        """
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
        """Update the cell's state based on the current simulation time.

        Args:
            t (float): Current simulation time in seconds
        """
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the hexagonal cell on the screen.

        Args:
            screen (pygame.Surface): Pygame surface to draw on
        """
        pass 