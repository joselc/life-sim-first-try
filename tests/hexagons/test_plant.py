"""Unit tests for the PlantHexagon class."""

import unittest
import math
from src.hexagons.plant import PlantHexagon
from tests.test_config import MOCK_CELL_SIZE, MOCK_COLORS


class TestPlantHexagon(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.plant = PlantHexagon(50, 50, MOCK_CELL_SIZE)

    def test_initialization(self):
        """Test that plant hexagon is initialized with correct attributes."""
        self.assertEqual(self.plant.cx, 50)
        self.assertEqual(self.plant.cy, 50)
        self.assertEqual(self.plant.a, MOCK_CELL_SIZE)
        self.assertEqual(self.plant.t, 0)
        self.assertTrue(0 <= self.plant.phase <= 2 * math.pi)

    def test_update(self):
        """Test that update method correctly updates time."""
        test_time = 1.5
        self.plant.update(test_time)
        self.assertEqual(self.plant.t, test_time)

    def test_color_oscillation(self):
        """Test that color oscillates between brown and green."""
        green = MOCK_COLORS['GREEN']
        brown = MOCK_COLORS['BROWN']
        
        # Test at t=0 with phase=0 (should be middle color)
        self.plant.t = 0
        self.plant.phase = 0
        color = self.plant.color
        self.assertEqual(len(color), 3)  # RGB color
        for i in range(3):
            expected = (brown[i] + green[i]) // 2
            self.assertAlmostEqual(color[i], expected, delta=1)
        
        # Test at t=pi/2 with phase=0 (should be greener)
        self.plant.t = math.pi/2
        color = self.plant.color
        # At least one color component should be closer to green than to brown
        differences = [abs(color[i] - green[i]) - abs(color[i] - brown[i]) for i in range(3)]
        self.assertTrue(any(diff < 0 for diff in differences), 
                       "Color should be closer to green in at least one component")
        
        # Test at t=pi with phase=0 (should be back to middle)
        self.plant.t = math.pi
        color = self.plant.color
        for i in range(3):
            expected = (brown[i] + green[i]) // 2
            self.assertAlmostEqual(color[i], expected, delta=1)


if __name__ == '__main__':
    unittest.main() 