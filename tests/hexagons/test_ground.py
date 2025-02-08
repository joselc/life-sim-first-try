"""Unit tests for the GroundHexagon class."""

import unittest
import pygame
from src.hexagons.ground import GroundHexagon
from tests.test_config import MOCK_CELL_SIZE, MOCK_COLORS


class TestGroundHexagon(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        pygame.init()
        self.screen = pygame.Surface((100, 100))
        self.ground = GroundHexagon(50, 50, MOCK_CELL_SIZE)

    def test_initialization(self):
        """Test that ground hexagon is initialized with correct attributes."""
        self.assertEqual(self.ground.cx, 50)
        self.assertEqual(self.ground.cy, 50)
        self.assertEqual(self.ground.a, MOCK_CELL_SIZE)

    def test_update_no_change(self):
        """Test that update method doesn't change the state."""
        initial_points = self.ground.points.copy()
        self.ground.update(1.5)
        self.assertEqual(self.ground.points, initial_points)

    def test_draw_color(self):
        """Test that the ground hexagon is drawn with the correct color."""
        # Draw the hexagon
        self.ground.draw(self.screen)
        
        # Get color at the center of the hexagon
        color_at_center = self.screen.get_at((50, 50))
        
        # Convert the color to RGB (ignoring alpha)
        drawn_color = color_at_center[:3]
        
        # Should match the brown color from config
        self.assertEqual(drawn_color, MOCK_COLORS['BROWN'])

    def tearDown(self):
        """Clean up after each test method."""
        pygame.quit()


if __name__ == '__main__':
    unittest.main() 