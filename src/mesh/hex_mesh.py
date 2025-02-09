"""Hexagonal grid system for the life simulation."""

import math
import random
from typing import List, Union
from ..hexagons.plant import PlantHexagon
from ..hexagons.ground import GroundHexagon
from ..config import PLANT_SPAWN_PROBABILITY
from ..hexagons.plant_states import PlantState


class HexMesh:
    """A hexagonal grid system that manages the life simulation world.

    This class creates and manages a grid of hexagonal cells, handling their
    placement and updates. The grid is composed of both plant
    and ground cells, randomly distributed based on spawn probability.

    Attributes:
        hexagons (List[Union[PlantHexagon, GroundHexagon]]): List of all hexagonal cells in the grid
    """

    def __init__(self, num_columns: int, num_rows: int, display_width: int, display_height: int) -> None:
        """Initialize the hexagonal grid.

        Creates a grid of hexagonal cells that fits within the specified display dimensions.
        The grid is centered horizontally on the screen.

        Args:
            num_columns (int): Number of columns in the grid
            num_rows (int): Number of rows in the grid
            display_width (int): Width of the display surface in pixels
            display_height (int): Height of the display surface in pixels
        """
        # Calculate side length 'a' so that vertical span fits display_height exactly
        a = display_height / (num_rows * math.sqrt(3))  # side length
        # Total grid width = 2*a + (num_columns - 1)*1.5*a
        grid_width = 2 * a + (num_columns - 1) * (1.5 * a)
        offset_x = (display_width - grid_width) / 2
        offset_y = 0  # even columns will touch top
        
        self.hexagons: List[Union[PlantHexagon, GroundHexagon]] = []
        for i in range(num_columns):
            for j in range(num_rows):
                # Compute center of hexagon for column i, row j
                cx = offset_x + a + i * (1.5 * a)
                if i % 2 == 0:
                    cy = offset_y + (a * math.sqrt(3) / 2) + j * (a * math.sqrt(3))
                else:
                    cy = offset_y + a * math.sqrt(3) + j * (a * math.sqrt(3))
                
                # Randomly choose between a plant hexagon and ground hexagon
                if random.random() < PLANT_SPAWN_PROBABILITY:
                    hexagon = PlantHexagon(cx, cy, a)
                else:
                    hexagon = GroundHexagon(cx, cy, a)
                
                self.hexagons.append(hexagon)

    def _convert_to_ground(self, index: int, plant: PlantHexagon) -> None:
        """Convert a dead plant to ground.
        
        Args:
            index (int): Index of the plant in the hexagons list
            plant (PlantHexagon): The plant hexagon to convert
        """
        ground = GroundHexagon(plant.cx, plant.cy, plant.a)
        self.hexagons[index] = ground

    def update(self, t: float) -> None:
        """Update all cells in the grid.

        Updates each cell and converts dead plants to ground.

        Args:
            t (float): Current simulation time in seconds
        """
        for i, hexagon in enumerate(self.hexagons):
            hexagon.update(t)
            
            # Convert dead plants to ground
            if isinstance(hexagon, PlantHexagon) and hexagon.state_manager.state == PlantState.DEAD:
                self._convert_to_ground(i, hexagon) 