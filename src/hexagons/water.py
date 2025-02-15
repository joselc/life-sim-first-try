"""Water hexagon implementation for the life simulation."""

from typing import Tuple
from .base import Hexagon
from ..config import COLORS


class WaterHexagon(Hexagon):
    """A hexagonal cell representing water in the life simulation.
    
    This class implements a static water cell that maintains a constant blue color.
    Water cells serve as terrain features and do not change over time.
    """

    def update(self, t: float) -> None:
        """Update the water cell's state (no-op as water doesn't change).

        Args:
            t (float): Current simulation time in seconds
        """
        pass

    @property
    def base_color(self) -> Tuple[int, int, int]:
        """Get the base color of the water cell.
        
        Returns:
            Tuple[int, int, int]: RGB color values (blue)
        """
        return COLORS['WATER']

    @property
    def detail_color(self) -> Tuple[int, int, int]:
        """Get the detail color (not used for water).
        
        Returns:
            Tuple[int, int, int]: RGB color values (black)
        """
        return (0, 0, 0)

    @property
    def detail_radius(self) -> float:
        """Get the detail radius (not used for water).
        
        Returns:
            float: Always 0.0 as water has no details
        """
        return 0.0 