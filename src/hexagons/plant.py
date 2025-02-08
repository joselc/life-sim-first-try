"""Plant cell implementation for the life simulation."""

import math
import random
from typing import Tuple
from .base import Hexagon
from ..config import COLORS


class PlantHexagon(Hexagon):
    """A hexagonal cell representing a plant in the life simulation.

    This class implements a plant cell that changes color over time,
    simulating growth and decay cycles. The color oscillates between
    brown and green based on a sinusoidal function with a random phase.

    Attributes:
        phase (float): Random phase offset for the color oscillation
        t (float): Current simulation time
    """

    def __init__(self, cx: float, cy: float, a: float) -> None:
        """Initialize a plant hexagonal cell.

        Args:
            cx (float): X-coordinate of the hexagon's center
            cy (float): Y-coordinate of the hexagon's center
            a (float): Length of the hexagon's side
        """
        super().__init__(cx, cy, a)
        self.phase = random.uniform(0, 2 * math.pi)
        self.t = 0

    def update(self, t: float) -> None:
        """Update the plant's state based on the current simulation time.

        Updates the internal time tracker used for color oscillation.

        Args:
            t (float): Current simulation time in seconds
        """
        self.t = t

    @property
    def color(self) -> Tuple[int, int, int]:
        """Get the current color of the plant.
        
        The color oscillates between brown and green based on the current time
        and phase offset.
        
        Returns:
            Tuple[int, int, int]: RGB color values
        """
        green = COLORS['GREEN']
        brown = COLORS['BROWN']
        factor = 0.5 * (1 + math.sin(self.t + self.phase))
        return (
            int(brown[0] * (1 - factor) + green[0] * factor),
            int(brown[1] * (1 - factor) + green[1] * factor),
            int(brown[2] * (1 - factor) + green[2] * factor)
        ) 