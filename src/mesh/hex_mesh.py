"""Hexagonal grid system for the life simulation."""

import math
import random
from typing import List, Union, Tuple
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
        num_columns (int): Number of columns in the grid
        num_rows (int): Number of rows in the grid
        grid_bounds (Tuple[float, float, float, float]): Grid boundaries (left, right, top, bottom)
        cell_size (float): Size of hexagon cells (side length)
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
        self.num_columns = num_columns
        self.num_rows = num_rows
        
        # Calculate side length 'a' so that vertical span fits display_height exactly
        self.cell_size = display_height / (num_rows * math.sqrt(3))  # side length
        # Total grid width = 2*a + (num_columns - 1)*1.5*a
        grid_width = 2 * self.cell_size + (num_columns - 1) * (1.5 * self.cell_size)
        self.offset_x = (display_width - grid_width) / 2
        self.offset_y = 0  # even columns will touch top
        
        # Calculate grid boundaries
        self.grid_bounds = (
            self.offset_x,  # left
            self.offset_x + grid_width,  # right
            self.offset_y,  # top
            display_height  # bottom
        )
        
        self.hexagons: List[Union[PlantHexagon, GroundHexagon]] = []
        for i in range(num_columns):
            for j in range(num_rows):
                # Compute center of hexagon for column i, row j
                cx = self.offset_x + self.cell_size + i * (1.5 * self.cell_size)
                if i % 2 == 0:
                    cy = self.offset_y + (self.cell_size * math.sqrt(3) / 2) + j * (self.cell_size * math.sqrt(3))
                else:
                    cy = self.offset_y + self.cell_size * math.sqrt(3) + j * (self.cell_size * math.sqrt(3))
                
                # Randomly choose between a plant hexagon and ground hexagon
                if random.random() < PLANT_SPAWN_PROBABILITY:
                    hexagon = PlantHexagon(cx, cy, self.cell_size)
                else:
                    hexagon = GroundHexagon(cx, cy, self.cell_size)
                
                self.hexagons.append(hexagon)

    def _is_position_valid(self, cx: float, cy: float) -> bool:
        """Check if a position is within the grid bounds.
        
        Args:
            cx (float): X-coordinate of the position
            cy (float): Y-coordinate of the position
            
        Returns:
            bool: True if the position is within bounds, False otherwise
        """
        left, right, top, bottom = self.grid_bounds
        # Add a small margin (half a cell) to account for hexagon extent
        margin = self.cell_size / 2
        return (left - margin <= cx <= right + margin and 
                top - margin <= cy <= bottom + margin)

    def _convert_plants_to_ground(self, dead_plants: List[Tuple[int, PlantHexagon]]) -> None:
        """Convert multiple dead plants to ground hexagons in bulk.
        
        Args:
            dead_plants (List[Tuple[int, PlantHexagon]]): List of (index, plant) pairs to convert
            
        Raises:
            ValueError: If any plant's position is outside the grid bounds
        """
        # First validate all positions
        for index, plant in dead_plants:
            if not self._is_position_valid(plant.cx, plant.cy):
                raise ValueError(
                    f"Plant position ({plant.cx}, {plant.cy}) is outside grid bounds {self.grid_bounds}"
                )
        
        # Then perform all conversions
        for index, plant in dead_plants:
            self.hexagons[index] = GroundHexagon(plant.cx, plant.cy, plant.a)

    def update(self, t: float) -> None:
        """Update all cells in the grid.

        Updates each cell and converts dead plants to ground in bulk.

        Args:
            t (float): Current simulation time in seconds
        """
        # First update all hexagons
        for hexagon in self.hexagons:
            hexagon.update(t)
        
        # Then identify and convert dead plants in bulk
        dead_plants = [
            (i, hexagon) for i, hexagon in enumerate(self.hexagons)
            if isinstance(hexagon, PlantHexagon) and hexagon.state_manager.state == PlantState.DEAD
        ]
        
        if dead_plants:
            self._convert_plants_to_ground(dead_plants) 