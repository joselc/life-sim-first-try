"""Unit tests for the HexMesh class."""

import unittest
import pygame
from src.mesh.hex_mesh import HexMesh
from src.hexagons.plant import PlantHexagon
from src.hexagons.ground import GroundHexagon
from tests.test_config import (
    MOCK_SCREEN_WIDTH,
    MOCK_SCREEN_HEIGHT,
    MOCK_COLUMNS,
    MOCK_ROWS
)


class TestHexMesh(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        pygame.init()
        self.screen = pygame.Surface((MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT))
        self.mesh = HexMesh(MOCK_COLUMNS, MOCK_ROWS, MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT)

    def test_initialization(self):
        """Test that mesh is initialized with correct number of hexagons."""
        expected_hexagons = MOCK_COLUMNS * MOCK_ROWS
        self.assertEqual(len(self.mesh.hexagons), expected_hexagons)

    def test_hexagon_types(self):
        """Test that all hexagons are of correct type."""
        for hexagon in self.mesh.hexagons:
            self.assertTrue(isinstance(hexagon, (PlantHexagon, GroundHexagon)))

    def test_grid_dimensions(self):
        """Test that the grid has reasonable dimensions.
        
        The grid should roughly fit within the screen bounds, allowing for some
        overlap at the edges due to hexagon geometry and offset calculations.
        """
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
        test_time = 1.5
        self.mesh.update(test_time)
        
        # Check that all plant hexagons have been updated
        for hexagon in self.mesh.hexagons:
            if isinstance(hexagon, PlantHexagon):
                self.assertEqual(hexagon.t, test_time)

    def test_draw(self):
        """Test that draw method executes without errors."""
        try:
            self.mesh.draw(self.screen)
            success = True
        except Exception:
            success = False
        self.assertTrue(success)

    def tearDown(self):
        """Clean up after each test method."""
        pygame.quit()


if __name__ == '__main__':
    unittest.main() 