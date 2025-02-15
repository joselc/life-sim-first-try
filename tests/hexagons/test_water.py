"""Unit tests for the WaterHexagon class."""

import unittest
from src.hexagons.water import WaterHexagon
from tests.test_config import MOCK_CELL_SIZE, MOCK_COLORS


class TestWaterHexagon(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.water = WaterHexagon(50, 50, MOCK_CELL_SIZE)

    def test_initialization(self):
        """Test that water hexagon is initialized with correct attributes."""
        self.assertEqual(self.water.cx, 50)
        self.assertEqual(self.water.cy, 50)
        self.assertEqual(self.water.a, MOCK_CELL_SIZE)

    def test_update_no_change(self):
        """Test that update method doesn't change the state."""
        initial_points = self.water.points.copy()
        self.water.update(1.5)
        self.assertEqual(self.water.points, initial_points)

    def test_color(self):
        """Test that the water hexagon returns the correct color."""
        self.assertEqual(self.water.base_color, MOCK_COLORS['WATER'])
        self.assertEqual(self.water.detail_color, (0, 0, 0))
        self.assertEqual(self.water.detail_radius, 0.0)


if __name__ == '__main__':
    unittest.main() 