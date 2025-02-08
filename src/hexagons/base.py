"""Base class for hexagonal cells in the life simulation."""

import math
from typing import List, Tuple, ClassVar
from ..config import COLORS


class Hexagon:
    """Base class for hexagonal cells in the life simulation.

    This class provides the basic structure and interface for hexagonal cells,
    including their geometric properties and state management.

    Attributes:
        cx (float): X-coordinate of the hexagon's center
        cy (float): Y-coordinate of the hexagon's center
        a (float): Length of the hexagon's side
        points (List[Tuple[float, float]]): List of (x, y) coordinates for the hexagon's vertices
    """

    # Default color for the hexagon
    DEFAULT_COLOR: ClassVar[Tuple[int, int, int]] = COLORS['BROWN']

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
        self._points: List[Tuple[float, float]] = [
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

    @property
    def points(self) -> List[Tuple[float, float]]:
        """Get the points that define the hexagon's shape.
        
        Returns:
            List[Tuple[float, float]]: List of (x, y) coordinates
        """
        return self._points

    @property
    def color(self) -> Tuple[int, int, int]:
        """Get the current color of the hexagon.
        
        Returns:
            Tuple[int, int, int]: RGB color values
        """
        return self.DEFAULT_COLOR 