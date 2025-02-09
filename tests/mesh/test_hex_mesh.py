"""Unit tests for the HexMesh class."""

import unittest
import random
from src.mesh.hex_mesh import HexMesh
from src.hexagons.plant import PlantHexagon
from src.hexagons.ground import GroundHexagon
from src.hexagons.plant_states import PlantState
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
            self.assertTrue(isinstance(hexagon, (PlantHexagon, GroundHexagon)))

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
            self.assertTrue(isinstance(drawn_hexagon, (PlantHexagon, GroundHexagon)))

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


if __name__ == '__main__':
    unittest.main() 