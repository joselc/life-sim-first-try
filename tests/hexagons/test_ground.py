"""Unit tests for the GroundHexagon class."""

import unittest
from src.hexagons.ground import GroundHexagon
from tests.test_config import MOCK_CELL_SIZE, MOCK_COLORS


class TestGroundHexagon(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
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

    def test_color(self):
        """Test that the ground hexagon returns the correct color."""
        self.assertEqual(self.ground.color, MOCK_COLORS['BROWN'])


if __name__ == '__main__':
    unittest.main() 