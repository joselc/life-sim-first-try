"""Hexagonal grid system for the life simulation."""

import math
import random
from typing import List, Union, Tuple, Set
from collections import deque
from ..hexagons.plant import PlantHexagon
from ..hexagons.ground import GroundHexagon
from ..hexagons.water import WaterHexagon
from ..config import (
    PLANT_SPAWN_PROBABILITY,
    WATER_SPAWN_PROBABILITY,
    MAX_WATER_PERCENTAGE
)
from ..hexagons.plant_states import PlantState


class HexMesh:
    """A hexagonal grid system that manages the life simulation world.

    This class creates and manages a grid of hexagonal cells, handling their
    placement and updates. The grid is composed of plant, ground, and water cells.

    Attributes:
        hexagons (List[Union[PlantHexagon, GroundHexagon, WaterHexagon]]): List of all hexagonal cells
        num_columns (int): Number of columns in the grid
        num_rows (int): Number of rows in the grid
        grid_bounds (Tuple[float, float, float, float]): Grid boundaries (left, right, top, bottom)
        cell_size (float): Size of hexagon cells (side length)
    """

    def __init__(self, num_columns: int, num_rows: int, display_width: int, display_height: int) -> None:
        """Initialize the hexagonal grid.
        
        Args:
            num_columns (int): Number of columns in the grid
            num_rows (int): Number of rows in the grid
            display_width (int): Width of the display area in pixels
            display_height (int): Height of the display area in pixels
        """
        self.num_columns = num_columns
        self.num_rows = num_rows
        self.display_width = display_width
        self.display_height = display_height
        
        # Calculate side length 'a' so that grid fits display
        hex_width = 2 * display_width / (num_columns * 1.75)  # Account for 0.75 spacing between columns
        self.cell_size = hex_width / 2  # side length is half the width
        
        # Calculate total grid dimensions
        grid_width = num_columns * self.cell_size * 1.75  # Total width with spacing
        grid_height = num_rows * self.cell_size * math.sqrt(3)  # Total height
        
        # Center the grid in the display
        self.offset_x = (display_width - grid_width) / 2
        self.offset_y = (display_height - grid_height) / 2
        
        # Calculate grid boundaries
        self.grid_bounds = (
            0,  # left bound at 0
            display_width,  # right bound at display width
            0,  # top bound at 0
            display_height  # bottom bound at display height
        )
        
        self.hexagons = []
        self._initialize_grid()

    def _initialize_grid(self) -> None:
        """Initialize the grid with ground hexagons and generate water groups."""
        self._create_ground_hexagons()
        
        # Generate water groups
        if random.random() < WATER_SPAWN_PROBABILITY:
            self._generate_water_groups()
        
        # Finally add plants on remaining ground hexagons
        self._add_plants()

    def _create_ground_hexagons(self) -> None:
        """Create initial grid of all ground hexagons using spaced pattern.
        
        The grid uses a columnar pattern where:
        - Hexagons are arranged in vertical columns
        - Each column is separated by 0.75 times the hexagon width
        - Alternate rows are shifted down by half the hexagon height
        """
        hex_width = 2 * self.cell_size  # Full width of a hexagon
        hex_height = self.cell_size * math.sqrt(3)  # Height of a hexagon
        
        for col in range(self.num_columns):
            for row in range(self.num_rows):
                # Calculate base position with spacing
                cx = self.offset_x + hex_width/2 + (col * hex_width * 0.75)  # Reduced spacing between columns
                cy = self.offset_y + hex_height/2 + (row * hex_height)
                
                # Shift alternate columns down by half height
                if col % 2 == 1:
                    cy += hex_height / 2
                
                self.hexagons.append(GroundHexagon(cx, cy, self.cell_size))

    def _get_hex_index(self, col: int, row: int) -> int:
        """Get the index of a hexagon in the grid array from its logical column and row.
        
        In column-major order, each column has num_rows elements, and we fill
        columns first before moving to the next column.
        
        Args:
            col (int): Logical column number (0 to num_columns-1)
            row (int): Logical row number (0 to num_rows-1)
            
        Returns:
            int: Index in the hexagons list, or -1 if invalid coordinates
        """
        if 0 <= col < self.num_columns and 0 <= row < self.num_rows:
            return col * self.num_rows + row
        return -1

    def _get_adjacent_indices(self, index: int) -> List[int]:
        """Get indices of adjacent hexagons using the columnar pattern.
        
        In this layout, each hexagon has 6 neighbors:
        - For even columns: neighbors are at same level and one level up
        - For odd columns: neighbors are at same level and one level down
        
        The grid is stored in column-major order, meaning we fill columns first,
        then move to the next column.
        
        Args:
            index (int): Index of the hexagon
            
        Returns:
            List[int]: List of valid adjacent hexagon indices
        """
        # For column-major order:
        # - Each column has num_rows elements
        # - Column number is index divided by num_rows
        # - Row number is remainder when divided by num_rows
        col = index // self.num_rows
        row = index % self.num_rows
        
        # Define adjacent positions based on column parity
        if col % 2 == 0:  # Even columns
            adjacent_positions = [
                (col-1, row-1),   # Top-left
                (col-1, row),     # Left
                (col, row+1),     # Bottom
                (col+1, row-1),   # Top-right
                (col+1, row),     # Right
                (col, row-1),     # Top
            ]
        else:  # Odd columns
            adjacent_positions = [
                (col-1, row),     # Left
                (col-1, row+1),   # Bottom-left
                (col, row+1),     # Bottom
                (col+1, row),     # Right
                (col+1, row+1),   # Bottom-right
                (col, row-1),     # Top
            ]
        
        # Filter out invalid indices
        valid_indices = []
        for c, r in adjacent_positions:
            idx = self._get_hex_index(c, r)
            if idx != -1:
                valid_indices.append(idx)
        
        return valid_indices

    def _grow_water_group(self, start_index: int, available_indices: Set[int]) -> Tuple[Set[int], Set[int]]:
        """Grow a water group from a starting position.
        
        Args:
            start_index (int): Starting position for the water group
            available_indices (Set[int]): Set of indices available for water placement
            
        Returns:
            Tuple[Set[int], Set[int]]: (Water group indices, Indices to remove from available)
        """
        # Calculate remaining capacity for water
        water_count = sum(1 for hex in self.hexagons if isinstance(hex, WaterHexagon))
        max_water = int(len(self.hexagons) * MAX_WATER_PERCENTAGE)
        remaining_capacity = max_water - water_count
        
        # If we can't add minimum size (4), return empty
        if remaining_capacity < 4:
            return set(), {start_index}
            
        # Initialize sets for tracking
        water_group = {start_index}
        indices_to_remove = {start_index}
        target_size = min(random.randint(4, 8), remaining_capacity)
        attempts = 0
        max_attempts = 20

        # Check if starting position is adjacent to existing water
        for adj_idx in self._get_adjacent_indices(start_index):
            if isinstance(self.hexagons[adj_idx], WaterHexagon):
                return set(), {start_index}

        # Try to grow the group
        while len(water_group) < target_size and attempts < max_attempts:
            attempts += 1
            current = random.choice(list(water_group))
            adjacent = self._get_adjacent_indices(current)
            
            # Filter for valid adjacent positions
            valid_adjacent = [idx for idx in adjacent 
                            if idx in available_indices 
                            and not any(isinstance(self.hexagons[adj_idx], WaterHexagon) 
                                      for adj_idx in self._get_adjacent_indices(idx))]
            
            if not valid_adjacent and len(water_group) < 4:
                return set(), indices_to_remove

            if valid_adjacent:
                # Add some random adjacent positions
                new_water = set(random.sample(valid_adjacent, 
                                          min(len(valid_adjacent), 
                                              min(random.randint(1, 3),
                                                  target_size - len(water_group)))))  # Ensure we don't exceed target
                water_group.update(new_water)
                indices_to_remove.update(new_water)

        # Return empty group if minimum size not reached
        if len(water_group) < 4:
            return set(), indices_to_remove

        return water_group, indices_to_remove

    def _generate_water_groups(self) -> None:
        """Generate water groups across the grid."""
        # Calculate maximum water coverage
        total_hexagons = len(self.hexagons)
        max_water_hexagons = int(total_hexagons * MAX_WATER_PERCENTAGE)
        water_count = sum(1 for hex in self.hexagons if isinstance(hex, WaterHexagon))
        
        # If we're already at or above the maximum, don't add more water
        if water_count >= max_water_hexagons:
            return
            
        attempts = 0
        max_attempts = total_hexagons // 2
        
        # Create set of available indices (excluding existing water)
        available_indices = {i for i, hex in enumerate(self.hexagons) 
                           if not isinstance(hex, WaterHexagon)}

        while attempts < max_attempts and water_count < max_water_hexagons:
            attempts += 1
            
            if not available_indices:
                break
                
            # Choose a random starting position
            start_index = random.choice(list(available_indices))
            
            # Check if adding a new group would exceed max water percentage
            if water_count + 4 > max_water_hexagons:  # Minimum group size is 4
                break
            
            # Try to grow a water group from this position
            water_group, indices_to_remove = self._grow_water_group(start_index, available_indices)
            
            # If group was successfully created and won't exceed limit, convert hexagons to water
            if water_group and (water_count + len(water_group)) <= max_water_hexagons:
                for idx in water_group:
                    self.hexagons[idx] = WaterHexagon(
                        self.hexagons[idx].cx,
                        self.hexagons[idx].cy,
                        self.hexagons[idx].a
                    )
                water_count += len(water_group)
            
            # Remove processed indices from available positions
            available_indices -= indices_to_remove

    def _add_plants(self) -> None:
        """Add plants to remaining ground hexagons."""
        for i, hexagon in enumerate(self.hexagons):
            if isinstance(hexagon, GroundHexagon) and random.random() < PLANT_SPAWN_PROBABILITY:
                self.hexagons[i] = PlantHexagon(hexagon.cx, hexagon.cy, hexagon.a)

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