"""Plant cell implementation for the life simulation."""

from typing import Tuple
from .base import Hexagon
from ..config import COLORS
from .plant_states import PlantStateManager


class PlantHexagon(Hexagon):
    """A hexagonal cell representing a plant in the life simulation.

    This class implements a plant cell that changes over time based on its state,
    simulating growth, maturity, flowering, and decay cycles.

    Attributes:
        state_manager (PlantStateManager): Manages the plant's lifecycle states
    """

    def __init__(self, cx: float, cy: float, a: float) -> None:
        """Initialize a plant hexagonal cell.

        Args:
            cx (float): X-coordinate of the hexagon's center
            cy (float): Y-coordinate of the hexagon's center
            a (float): Length of the hexagon's side
        """
        super().__init__(cx, cy, a)
        self.state_manager = PlantStateManager()

    def update(self, t: float) -> None:
        """Update the plant's state based on the current simulation time.

        Updates the plant's state manager to handle lifecycle transitions.

        Args:
            t (float): Current simulation time in seconds
        """
        self.state_manager.update(t)

    @property
    def color(self) -> Tuple[int, int, int]:
        """Get the current color of the plant based on its state.
        
        The color transitions between brown and green based on the plant's
        current state and health/growth factors.
        
        Returns:
            Tuple[int, int, int]: RGB color values
        """
        green = COLORS['GREEN']
        brown = COLORS['BROWN']
        factor = self.state_manager.color_factor
        
        return (
            int(brown[0] * (1 - factor) + green[0] * factor),
            int(brown[1] * (1 - factor) + green[1] * factor),
            int(brown[2] * (1 - factor) + green[2] * factor)
        ) 