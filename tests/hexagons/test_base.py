"""Unit tests for the base Hexagon class."""

import unittest
import math
from src.hexagons.base import Hexagon
from tests.test_config import MOCK_CELL_SIZE, MOCK_COLORS


class TestHexagon(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.hexagon = Hexagon(50, 50, MOCK_CELL_SIZE)

    def test_initialization(self):
        """Test that hexagon is initialized with correct attributes."""
        self.assertEqual(self.hexagon.cx, 50)
        self.assertEqual(self.hexagon.cy, 50)
        self.assertEqual(self.hexagon.a, MOCK_CELL_SIZE)
        self.assertEqual(len(self.hexagon.points), 6)  # Hexagon should have 6 vertices

    def test_vertex_positions(self):
        """Test that vertex positions are calculated correctly."""
        # Test first vertex (rightmost point)
        expected_x = self.hexagon.cx + self.hexagon.a
        expected_y = self.hexagon.cy
        self.assertAlmostEqual(self.hexagon.points[0][0], expected_x)
        self.assertAlmostEqual(self.hexagon.points[0][1], expected_y)

        # Test second vertex (bottom right)
        expected_x = self.hexagon.cx + self.hexagon.a/2
        expected_y = self.hexagon.cy + (self.hexagon.a * math.sqrt(3) / 2)
        self.assertAlmostEqual(self.hexagon.points[1][0], expected_x)
        self.assertAlmostEqual(self.hexagon.points[1][1], expected_y)

    def test_hexagon_symmetry(self):
        """Test that the hexagon vertices are symmetrical."""
        # Test horizontal symmetry by checking distances from center
        left_dist = abs(self.hexagon.points[3][0] - self.hexagon.cx)   # Distance from center to left point
        right_dist = abs(self.hexagon.points[0][0] - self.hexagon.cx)  # Distance from center to right point
        self.assertAlmostEqual(left_dist, right_dist)

        # Test vertical symmetry by checking distances from center
        top_dist = abs(self.hexagon.points[4][1] - self.hexagon.cy)    # Distance from center to top point
        bottom_dist = abs(self.hexagon.points[1][1] - self.hexagon.cy) # Distance from center to bottom point
        self.assertAlmostEqual(top_dist, bottom_dist)

    def test_color_property(self):
        """Test that the default color is returned correctly."""
        self.assertEqual(self.hexagon.color, MOCK_COLORS['BROWN'])

    def test_points_property(self):
        """Test that points property returns the correct points."""
        points = self.hexagon.points
        self.assertEqual(len(points), 6)
        self.assertEqual(points, self.hexagon._points)

    def test_update_method(self):
        """Test that update method exists and can be called."""
        try:
            self.hexagon.update(1.0)
            success = True
        except Exception:
            success = False
        self.assertTrue(success)


if __name__ == '__main__':
    unittest.main() 