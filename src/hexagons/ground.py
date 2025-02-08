"""Ground cell implementation for the life simulation."""

from typing import Tuple
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

    @property
    def color(self) -> Tuple[int, int, int]:
        """Get the color of the ground cell.
        
        Returns:
            Tuple[int, int, int]: RGB color values (brown)
        """
        return COLORS['BROWN'] 