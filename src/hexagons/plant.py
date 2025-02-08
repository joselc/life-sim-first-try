"""Plant cell implementation for the life simulation."""

from typing import Tuple
from .base import Hexagon
from ..config import COLORS
from .plant_states import PlantStateManager, PlantState


class PlantHexagon(Hexagon):
    """A hexagonal cell representing a plant in the life simulation.

    This class implements a plant cell that changes over time based on its state,
    simulating growth, maturity, flowering, and decay cycles.

    Attributes:
        state_manager (PlantStateManager): Manages the plant's lifecycle states
    """

    # Visual detail constants
    SEED_DOT_RADIUS = 0.15    # Relative to hexagon size
    GROWING_DOT_RADIUS = 0.45  # Relative to hexagon size (increased from 0.3)

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
    def base_color(self) -> Tuple[int, int, int]:
        """Get the base color of the hexagon."""
        if self.state_manager.state == PlantState.MATURE:
            return COLORS['MATURE']
        elif self.state_manager.state == PlantState.DYING:
            return COLORS['DYING']
        elif self.state_manager.state == PlantState.DEAD:
            return COLORS['DEAD']
        else:
            return COLORS['BROWN']  # Ground color for SEED and GROWING states

    @property
    def detail_color(self) -> Tuple[int, int, int]:
        """Get the color of the detail (dot) in the center."""
        if self.state_manager.state == PlantState.SEED:
            return COLORS['YELLOW']  # New color for seed dot
        elif self.state_manager.state == PlantState.GROWING:
            return COLORS['GROWING']
        return (0, 0, 0)  # Black for other states (won't be visible)

    @property
    def detail_radius(self) -> float:
        """Get the radius of the detail (dot) relative to hexagon size."""
        if self.state_manager.state == PlantState.SEED:
            return self.SEED_DOT_RADIUS
        elif self.state_manager.state == PlantState.GROWING:
            return self.GROWING_DOT_RADIUS
        return 0.0  # No dot for other states 