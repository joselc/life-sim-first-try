"""Unit tests for the HexMesh class."""

import unittest
import random
import math
from src.mesh.hex_mesh import HexMesh
from src.hexagons.plant import PlantHexagon
from src.hexagons.ground import GroundHexagon
from src.hexagons.plant_states import PlantState
from src.hexagons.water import WaterHexagon
from tests.renderers.test_base import MockRenderer
from tests.test_config import (
    MOCK_SCREEN_WIDTH,
    MOCK_SCREEN_HEIGHT,
    MOCK_COLUMNS,
    MOCK_ROWS
)
from unittest.mock import patch, Mock


class TestHexMesh(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Set fixed seed for consistent plant generation
        random.seed(12345)
        self.mesh = HexMesh(MOCK_COLUMNS, MOCK_ROWS, MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT)
        self.renderer = MockRenderer()

    def tearDown(self):
        """Clean up after each test."""
        # Reset the random seed
        random.seed()

    def test_initialization(self):
        """Test that mesh is initialized with correct number of hexagons."""
        expected_hexagons = MOCK_COLUMNS * MOCK_ROWS
        self.assertEqual(len(self.mesh.hexagons), expected_hexagons)

    def test_hexagon_types(self):
        """Test that all hexagons are of correct type."""
        for hexagon in self.mesh.hexagons:
            self.assertTrue(isinstance(hexagon, (PlantHexagon, GroundHexagon, WaterHexagon)))

    def test_grid_dimensions(self):
        """Test that the grid has reasonable dimensions."""
        # Find the leftmost, rightmost, topmost, and bottommost points
        left = min(h.cx - h.a for h in self.mesh.hexagons)
        right = max(h.cx + h.a for h in self.mesh.hexagons)
        top = min(h.cy - h.a for h in self.mesh.hexagons)
        bottom = max(h.cy + h.a for h in self.mesh.hexagons)

        # Grid should roughly fit within screen bounds
        # Allow for a margin of error of one cell size
        margin = self.mesh.hexagons[0].a
        self.assertGreaterEqual(left, -margin)
        self.assertLessEqual(right, MOCK_SCREEN_WIDTH + margin)
        self.assertGreaterEqual(top, -margin)
        self.assertLessEqual(bottom, MOCK_SCREEN_HEIGHT + margin)

        # Also verify that most of the grid is within the screen
        self.assertLess(left, MOCK_SCREEN_WIDTH)
        self.assertGreater(right, 0)
        self.assertLess(top, MOCK_SCREEN_HEIGHT)
        self.assertGreater(bottom, 0)

    def test_update_propagation(self):
        """Test that update calls are propagated to all hexagons."""
        # Replace all hexagons with mocks
        mock_hexagons = []
        for hexagon in self.mesh.hexagons:
            mock = Mock()
            mock.cx = hexagon.cx
            mock.cy = hexagon.cy
            mock.a = hexagon.a
            mock_hexagons.append(mock)
        self.mesh.hexagons = mock_hexagons

        # Update the mesh
        update_time = 0.1
        self.mesh.update(update_time)

        # Verify that update was called on each hexagon
        for mock in mock_hexagons:
            mock.update.assert_called_once_with(update_time)

    def test_rendering(self):
        """Test that all hexagons can be rendered."""
        # Render all hexagons
        for hexagon in self.mesh.hexagons:
            self.renderer.draw_hexagon(hexagon, show_grid=True)
        
        # Check that all hexagons were rendered
        self.assertEqual(len(self.renderer.drawn_hexagons), len(self.mesh.hexagons))
        
        # Check that each hexagon was rendered with grid
        for drawn_hexagon, show_grid in self.renderer.drawn_hexagons:
            self.assertTrue(show_grid)
            self.assertTrue(isinstance(drawn_hexagon, (PlantHexagon, GroundHexagon, WaterHexagon)))

    def test_dead_plant_conversion(self):
        """Test that dead plants are converted to ground."""
        # Find a plant hexagon
        plant_index = None
        for i, hexagon in enumerate(self.mesh.hexagons):
            if isinstance(hexagon, PlantHexagon):
                plant_index = i
                break
        
        if plant_index is None:
            # Create a plant if none exists
            plant = PlantHexagon(50, 50, 10)
            self.mesh.hexagons[0] = plant
            plant_index = 0
        
        plant = self.mesh.hexagons[plant_index]
        original_position = (plant.cx, plant.cy, plant.a)
        
        # Set plant to dead state
        plant.state_manager.state = PlantState.DEAD
        
        # Update should trigger conversion
        self.mesh.update(0.1)
        
        # Verify conversion
        converted = self.mesh.hexagons[plant_index]
        self.assertIsInstance(converted, GroundHexagon)
        self.assertEqual((converted.cx, converted.cy, converted.a), original_position)

    def test_multiple_dead_plant_conversions(self):
        """Test that multiple dead plants are converted to ground correctly."""
        # Create a mesh with only plants
        with patch('random.random', return_value=0.0):  # Ensure all cells are plants
            test_mesh = HexMesh(2, 2, MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT)
        
        # Set some plants to dead state
        dead_indices = [0, 2]  # First and third plants
        for i in dead_indices:
            plant = test_mesh.hexagons[i]
            plant.state_manager.state = PlantState.DEAD
        
        # Update should convert dead plants
        test_mesh.update(0.1)
        
        # Verify conversions
        for i in dead_indices:
            self.assertIsInstance(test_mesh.hexagons[i], GroundHexagon)
        
        # Verify other plants remain unchanged
        for i in range(len(test_mesh.hexagons)):
            if i not in dead_indices:
                self.assertIsInstance(test_mesh.hexagons[i], PlantHexagon)

    def test_position_preservation_after_conversion(self):
        """Test that converted ground hexagons maintain the same position as the original plant."""
        # Create a plant and record its position
        plant = PlantHexagon(50, 50, 10)
        self.mesh.hexagons[0] = plant
        original_points = plant.points.copy()
        
        # Set to dead state and update
        plant.state_manager.state = PlantState.DEAD
        self.mesh.update(0.1)
        
        # Verify position is maintained
        ground = self.mesh.hexagons[0]
        self.assertIsInstance(ground, GroundHexagon)
        self.assertEqual(ground.points, original_points)

    def test_grid_bounds_initialization(self):
        """Test that grid boundaries are correctly initialized."""
        # Check that bounds are properly set
        left, right, top, bottom = self.mesh.grid_bounds
        
        # Verify basic bounds properties
        self.assertLess(left, right)  # Left bound should be less than right
        self.assertLess(top, bottom)  # Top bound should be less than bottom
        self.assertEqual(bottom, MOCK_SCREEN_HEIGHT)  # Bottom should match screen height
        self.assertEqual(top, 0)  # Top should be 0
        
        # Verify grid is centered horizontally
        grid_width = right - left
        expected_left = (MOCK_SCREEN_WIDTH - grid_width) / 2
        self.assertAlmostEqual(left, expected_left)

    def test_position_validation_within_bounds(self):
        """Test that positions within grid bounds are validated correctly."""
        # Get a known valid position (center of first hexagon)
        valid_hexagon = self.mesh.hexagons[0]
        
        # Test center position
        self.assertTrue(
            self.mesh._is_position_valid(valid_hexagon.cx, valid_hexagon.cy),
            "Center position should be valid"
        )
        
        # Test positions near the edges but within bounds
        left, right, top, bottom = self.mesh.grid_bounds
        margin = self.mesh.cell_size / 2
        
        # Test various valid positions
        valid_positions = [
            (left + margin, top + margin),  # Top-left with margin
            (right - margin, top + margin),  # Top-right with margin
            (left + margin, bottom - margin),  # Bottom-left with margin
            (right - margin, bottom - margin),  # Bottom-right with margin
            ((left + right) / 2, (top + bottom) / 2),  # Center of grid
        ]
        
        for x, y in valid_positions:
            self.assertTrue(
                self.mesh._is_position_valid(x, y),
                f"Position ({x}, {y}) should be valid"
            )

    def test_position_validation_outside_bounds(self):
        """Test that positions outside grid bounds are invalidated correctly."""
        left, right, top, bottom = self.mesh.grid_bounds
        margin = self.mesh.cell_size / 2
        
        # Test various invalid positions
        invalid_positions = [
            (left - margin * 2, top),  # Too far left
            (right + margin * 2, top),  # Too far right
            (left, top - margin * 2),  # Too far up
            (right, bottom + margin * 2),  # Too far down
            (float('-inf'), 0),  # Extreme left
            (float('inf'), 0),  # Extreme right
            (0, float('-inf')),  # Extreme top
            (0, float('inf')),  # Extreme bottom
        ]
        
        for x, y in invalid_positions:
            self.assertFalse(
                self.mesh._is_position_valid(x, y),
                f"Position ({x}, {y}) should be invalid"
            )

    def test_convert_invalid_position(self):
        """Test that converting a plant with invalid position raises ValueError."""
        # Create a plant with invalid position
        left, right, top, bottom = self.mesh.grid_bounds
        invalid_plant = PlantHexagon(
            left - self.mesh.cell_size * 2,  # Way outside left bound
            top,
            self.mesh.cell_size
        )
        invalid_plant.state_manager.state = PlantState.DEAD
        
        # Try to convert the invalid plant
        with self.assertRaises(ValueError) as context:
            self.mesh._convert_plants_to_ground([(0, invalid_plant)])
        
        # Verify error message contains position and bounds information
        error_msg = str(context.exception)
        self.assertIn("outside grid bounds", error_msg)
        self.assertIn(str(self.mesh.grid_bounds), error_msg)

    def test_convert_edge_case_positions(self):
        """Test conversion of plants at edge positions within the margin."""
        left, right, top, bottom = self.mesh.grid_bounds
        margin = self.mesh.cell_size / 2
        
        # Create plants at edge positions but within margin
        edge_positions = [
            (left - margin + 0.1, (top + bottom) / 2),  # Just inside left margin
            (right + margin - 0.1, (top + bottom) / 2),  # Just inside right margin
            ((left + right) / 2, top - margin + 0.1),  # Just inside top margin
            ((left + right) / 2, bottom + margin - 0.1),  # Just inside bottom margin
        ]
        
        for i, (x, y) in enumerate(edge_positions):
            # Create a plant at the edge position
            plant = PlantHexagon(x, y, self.mesh.cell_size)
            plant.state_manager.state = PlantState.DEAD
            
            # Verify conversion succeeds
            try:
                self.mesh._convert_plants_to_ground([(i, plant)])
                success = True
            except ValueError:
                success = False
            
            self.assertTrue(
                success,
                f"Conversion should succeed for position ({x}, {y})"
            )

    def test_bulk_conversion_validation(self):
        """Test that bulk conversion validates all positions before converting any."""
        # Create a mesh with no water
        with patch('random.random', return_value=0.0), \
             patch('src.mesh.hex_mesh.WATER_SPAWN_PROBABILITY', 0.0):  # Ensure no water generation
            self.mesh = HexMesh(MOCK_COLUMNS, MOCK_ROWS, MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT)
        
        # Create a mix of valid and invalid plants
        valid_plant = self.mesh.hexagons[0]
        if not isinstance(valid_plant, PlantHexagon):
            valid_plant = PlantHexagon(valid_plant.cx, valid_plant.cy, valid_plant.a)
        
        left, right, top, bottom = self.mesh.grid_bounds
        invalid_plant = PlantHexagon(
            right + self.mesh.cell_size * 2,  # Way outside right bound
            top,
            self.mesh.cell_size
        )
        
        # Set both plants as dead
        valid_plant.state_manager.state = PlantState.DEAD
        invalid_plant.state_manager.state = PlantState.DEAD
        
        # Try to convert both plants
        with self.assertRaises(ValueError):
            self.mesh._convert_plants_to_ground([(0, valid_plant), (1, invalid_plant)])
        
        # Verify that no conversions took place (the valid plant should not have been converted)
        self.assertIsInstance(self.mesh.hexagons[0], PlantHexagon)

    def test_water_hexagon_generation(self):
        """Test that water hexagons are generated correctly."""
        # Use a higher spawn probability to ensure water generation
        with patch('random.random', return_value=0.5), \
             patch('src.mesh.hex_mesh.WATER_SPAWN_PROBABILITY', 0.8):  # 80% chance
            mesh = HexMesh(MOCK_COLUMNS, MOCK_ROWS, MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT)
            
            # Count water hexagons
            water_count = sum(1 for hex in mesh.hexagons if isinstance(hex, WaterHexagon))
            
            # Verify water hexagons exist
            self.assertGreater(water_count, 0, "No water hexagons were generated")
            
            # Verify water coverage doesn't exceed maximum
            max_water = int(len(mesh.hexagons) * 0.3)  # 30% maximum
            self.assertLessEqual(water_count, max_water, 
                               f"Water coverage ({water_count}) exceeds maximum ({max_water})")

    def test_water_group_size(self):
        """Test that water groups meet minimum size requirement."""
        # Use a higher spawn probability to ensure water generation
        with patch('src.mesh.hex_mesh.WATER_SPAWN_PROBABILITY', 0.8):
            mesh = HexMesh(MOCK_COLUMNS, MOCK_ROWS, MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT)
            
            # Find water groups by checking adjacency
            water_groups = []
            checked = set()
            
            for i, hex in enumerate(mesh.hexagons):
                if isinstance(hex, WaterHexagon) and i not in checked:
                    # Start a new group
                    group = {i}
                    edge = {i}
                    checked.add(i)
                    
                    # Grow group to include all adjacent water hexagons
                    while edge:
                        current = edge.pop()
                        adjacent = mesh._get_adjacent_indices(current)
                        for adj_idx in adjacent:
                            if (adj_idx not in checked and 
                                isinstance(mesh.hexagons[adj_idx], WaterHexagon)):
                                group.add(adj_idx)
                                edge.add(adj_idx)
                                checked.add(adj_idx)
                    
                    water_groups.append(group)
            
            # Verify each group has at least 4 hexagons
            for group in water_groups:
                self.assertGreaterEqual(len(group), 4,
                                      f"Water group size ({len(group)}) is less than minimum (4)")

    def test_water_adjacency(self):
        """Test that water hexagons in a group are properly adjacent."""
        # Use a higher spawn probability to ensure water generation
        with patch('src.mesh.hex_mesh.WATER_SPAWN_PROBABILITY', 0.8):
            mesh = HexMesh(MOCK_COLUMNS, MOCK_ROWS, MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT)
            
            # Find a water hexagon
            water_indices = [i for i, hex in enumerate(mesh.hexagons) 
                            if isinstance(hex, WaterHexagon)]
            
            if water_indices:  # If we found water hexagons
                start_idx = water_indices[0]
                
                # Get adjacent indices
                adjacent = mesh._get_adjacent_indices(start_idx)
                
                # Verify at least one adjacent hexagon is also water
                adjacent_water = any(isinstance(mesh.hexagons[idx], WaterHexagon) 
                                   for idx in adjacent)
                
                self.assertTrue(adjacent_water, 
                              "Water hexagon found with no adjacent water hexagons")

    def test_terrain_distribution(self):
        """Test the distribution of different terrain types."""
        # Use a higher spawn probability to ensure water generation
        with patch('src.mesh.hex_mesh.WATER_SPAWN_PROBABILITY', 0.8):
            mesh = HexMesh(MOCK_COLUMNS, MOCK_ROWS, MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT)
            
            # Count each type of terrain
            water_count = sum(1 for hex in mesh.hexagons if isinstance(hex, WaterHexagon))
            plant_count = sum(1 for hex in mesh.hexagons if isinstance(hex, PlantHexagon))
            ground_count = sum(1 for hex in mesh.hexagons if isinstance(hex, GroundHexagon))
            
            total = len(mesh.hexagons)
            
            # Verify counts add up to total
            self.assertEqual(water_count + plant_count + ground_count, total)
            
            # Verify water percentage
            water_percentage = water_count / total
            self.assertLessEqual(water_percentage, 0.3)

    def test_water_generation_edge_cases(self):
        """Test edge cases in water generation."""
        # Test with very high spawn probability
        with patch('src.mesh.hex_mesh.WATER_SPAWN_PROBABILITY', 1.0):
            mesh = HexMesh(MOCK_COLUMNS, MOCK_ROWS, MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT)
            water_count = sum(1 for hex in mesh.hexagons if isinstance(hex, WaterHexagon))
            total = len(mesh.hexagons)
            # Even with 100% spawn probability, should not exceed max percentage
            self.assertLessEqual(water_count / total, 0.3)

        # Test with very low spawn probability
        with patch('src.mesh.hex_mesh.WATER_SPAWN_PROBABILITY', 0.01):
            mesh = HexMesh(MOCK_COLUMNS, MOCK_ROWS, MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT)
            water_groups = self._find_water_groups(mesh)
            # Any groups that do form should still meet minimum size
            for group in water_groups:
                self.assertGreaterEqual(len(group), 4)

    def test_water_group_formation_at_boundaries(self):
        """Test water group formation at grid boundaries."""
        # Use a higher spawn probability to ensure water generation
        with patch('src.mesh.hex_mesh.WATER_SPAWN_PROBABILITY', 0.8):
            mesh = HexMesh(MOCK_COLUMNS, MOCK_ROWS, MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT)
            
            # Find water groups at edges
            edge_groups = []
            for i, hex in enumerate(mesh.hexagons):
                if isinstance(hex, WaterHexagon):
                    # Check if hexagon is at edge (first/last row/column)
                    row = i // MOCK_COLUMNS
                    col = i % MOCK_COLUMNS
                    if (row == 0 or row == MOCK_ROWS - 1 or 
                        col == 0 or col == MOCK_COLUMNS - 1):
                        group = self._find_water_group_from_index(mesh, i)
                        if group not in edge_groups:
                            edge_groups.append(group)
            
            # Verify edge groups meet size requirements
            for group in edge_groups:
                self.assertGreaterEqual(len(group), 4)

    def test_water_group_connectivity(self):
        """Test that water groups are fully connected with no isolated hexagons."""
        # Use a higher spawn probability to ensure water generation
        with patch('src.mesh.hex_mesh.WATER_SPAWN_PROBABILITY', 0.8):
            mesh = HexMesh(MOCK_COLUMNS, MOCK_ROWS, MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT)
            
            # Find all water groups
            water_groups = self._find_water_groups(mesh)
            
            # Get all water hexagon indices
            water_indices = {i for i, hex in enumerate(mesh.hexagons) 
                            if isinstance(hex, WaterHexagon)}
            
            # Verify all water hexagons belong to exactly one group
            grouped_indices = set().union(*water_groups) if water_groups else set()
            self.assertEqual(water_indices, grouped_indices)

    def test_water_group_shape(self):
        """Test that water groups form reasonable lake-like shapes."""
        # Use a higher spawn probability to ensure water generation
        with patch('src.mesh.hex_mesh.WATER_SPAWN_PROBABILITY', 0.8):
            mesh = HexMesh(MOCK_COLUMNS, MOCK_ROWS, MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT)
            
            water_groups = self._find_water_groups(mesh)
            
            for group in water_groups:
                # Calculate group metrics
                metrics = self._calculate_group_metrics(mesh, group)
                
                # Verify group is not just a straight line
                self.assertGreater(metrics['width_height_ratio'], 0.3,
                                 "Water group is too linear")
                
                # Verify group is reasonably compact
                self.assertLess(metrics['max_distance_ratio'], 3.0,
                              "Water group is too spread out")

    def test_water_group_growth_with_obstacles(self):
        """Test water group growth when encountering obstacles."""
        # Create a mesh with a specific pattern of hexagons
        with patch('random.random', return_value=0.0):  # Ensure no random water initially
            mesh = HexMesh(3, 3, MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT)
        
        # Create a water hexagon surrounded by ground
        center_index = 4  # Center of 3x3 grid
        mesh.hexagons[center_index] = WaterHexagon(
            mesh.hexagons[center_index].cx,
            mesh.hexagons[center_index].cy,
            mesh.hexagons[center_index].a
        )
        
        # Try to grow the water group
        adjacent_indices = mesh._get_adjacent_indices(center_index)
        water_group, removed = mesh._grow_water_group(center_index, set(adjacent_indices))
        
        # Verify water didn't spread where it shouldn't
        water_count = sum(1 for hex in mesh.hexagons if isinstance(hex, WaterHexagon))
        self.assertEqual(water_count, 1, "Water should not spread when surrounded by ground")

    def test_water_group_generation_limits(self):
        """Test water group generation respects maximum coverage limits."""
        # Create a mesh with maximum water coverage
        with patch('random.random', return_value=0.0), \
             patch('src.mesh.hex_mesh.WATER_SPAWN_PROBABILITY', 0.0):  # Ensure no initial water
            mesh = HexMesh(MOCK_COLUMNS, MOCK_ROWS, MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT)
        
        # Add water hexagons up to the maximum limit
        max_water = int(len(mesh.hexagons) * 0.3)  # 30% maximum
        for i in range(max_water):
            mesh.hexagons[i] = WaterHexagon(
                mesh.hexagons[i].cx,
                mesh.hexagons[i].cy,
                mesh.hexagons[i].a
            )
        
        # Try to generate more water groups with high probability
        with patch('random.random', return_value=1.0), \
             patch('src.mesh.hex_mesh.WATER_SPAWN_PROBABILITY', 1.0):
            mesh._generate_water_groups()
        
        # Verify water coverage hasn't exceeded the maximum
        water_count = sum(1 for hex in mesh.hexagons if isinstance(hex, WaterHexagon))
        self.assertEqual(water_count, max_water, "Water coverage should not exceed maximum")

    def test_find_water_groups_empty(self):
        """Test finding water groups when no water exists."""
        # Create a mesh with no water by patching both random values
        with patch('random.random', return_value=0.0), \
             patch('src.mesh.hex_mesh.WATER_SPAWN_PROBABILITY', 0.0):  # Set to 0.0 to prevent water generation
            mesh = HexMesh(MOCK_COLUMNS, MOCK_ROWS, MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT)

        # Find water groups
        water_groups = self._find_water_groups(mesh)

        # Verify no groups were found
        self.assertEqual(len(water_groups), 0, "Should find no water groups in empty mesh")

    def test_find_water_group_from_index_invalid(self):
        """Test finding water group from an invalid starting index."""
        # Create a mesh with known water positions
        with patch('random.random', return_value=0.0):
            mesh = HexMesh(3, 3, MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT)
        
        # Place water hexagons in specific positions
        water_indices = [0, 1, 3, 4]  # Forms a 2x2 water group
        for i in water_indices:
            mesh.hexagons[i] = WaterHexagon(
                mesh.hexagons[i].cx,
                mesh.hexagons[i].cy,
                mesh.hexagons[i].a
            )
        
        # Try to find water group from a non-water hexagon
        non_water_index = 8  # Bottom-right corner
        group = self._find_water_group_from_index(mesh, non_water_index)
        
        # Verify empty group is returned
        self.assertEqual(len(group), 0, "Should return empty group for non-water hexagon")

    def test_find_water_group_from_index_complete(self):
        """Test finding complete water group from any starting index."""
        # Create a mesh with known water positions
        with patch('random.random', return_value=0.0):
            mesh = HexMesh(3, 3, MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT)
        
        # Create an L-shaped water group
        water_indices = {0, 1, 3}  # L-shape in top-left
        for i in water_indices:
            mesh.hexagons[i] = WaterHexagon(
                mesh.hexagons[i].cx,
                mesh.hexagons[i].cy,
                mesh.hexagons[i].a
            )
        
        # Find group starting from each water hexagon
        for start_index in water_indices:
            group = self._find_water_group_from_index(mesh, start_index)
            self.assertEqual(group, water_indices,
                           f"Water group from index {start_index} should find all connected water")

    def _find_water_groups(self, mesh):
        """Helper method to find all water groups in the mesh."""
        water_groups = []
        checked_indices = set()
        
        for i in range(len(mesh.hexagons)):
            if isinstance(mesh.hexagons[i], WaterHexagon) and i not in checked_indices:
                group = self._find_water_group_from_index(mesh, i)
                water_groups.append(group)
                checked_indices.update(group)
        
        return water_groups

    def _find_water_group_from_index(self, mesh, start_index):
        """Helper method to find a water group starting from an index."""
        if not isinstance(mesh.hexagons[start_index], WaterHexagon):
            return set()
        
        group = {start_index}
        to_check = {start_index}
        
        while to_check:
            current = to_check.pop()
            adjacent_indices = mesh._get_adjacent_indices(current)
            
            for adj_idx in adjacent_indices:
                if (adj_idx not in group and 
                    isinstance(mesh.hexagons[adj_idx], WaterHexagon)):
                    group.add(adj_idx)
                    to_check.add(adj_idx)
        
        return group

    def _calculate_group_metrics(self, mesh, group):
        """Helper method to calculate metrics for a water group."""
        if not group:
            return {'width_height_ratio': 0, 'max_distance_ratio': float('inf')}
        
        # Get coordinates of all hexagons in group
        coords = [(mesh.hexagons[i].cx, mesh.hexagons[i].cy) for i in group]
        xs, ys = zip(*coords)
        
        # Calculate dimensions
        width = max(xs) - min(xs)
        height = max(ys) - min(ys)
        if height == 0:
            height = 1  # Avoid division by zero
        
        # Calculate center point
        center_x = sum(xs) / len(xs)
        center_y = sum(ys) / len(ys)
        
        # Calculate maximum distance from center
        max_distance = max(math.sqrt((x - center_x)**2 + (y - center_y)**2)
                         for x, y in coords)
        ideal_radius = math.sqrt(len(group) * mesh.cell_size**2 / math.pi)
        
        return {
            'width_height_ratio': min(width, height) / max(width, height),
            'max_distance_ratio': max_distance / ideal_radius
        }


if __name__ == '__main__':
    unittest.main() 