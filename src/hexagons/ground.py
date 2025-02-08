import pygame
from .base import Hexagon
from ..config import COLORS


class GroundHexagon(Hexagon):
    """A hexagonal cell representing ground or soil in the life simulation.

    This class implements a static ground cell that maintains a constant brown color.
    Ground cells serve as the base terrain in the simulation and do not change over time.
    """

    def update(self, t: float) -> None:
        """Update the ground cell's state (no-op as ground doesn't change).

        Args:
            t (float): Current simulation time in seconds
        """
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the ground cell on the screen.

        Renders the hexagon with a static brown color and a grid line border.

        Args:
            screen (pygame.Surface): Pygame surface to draw on
        """
        pygame.draw.polygon(screen, COLORS['BROWN'], self.points, 0)
        pygame.draw.polygon(screen, COLORS['GRID_LINES'], self.points, 1) 