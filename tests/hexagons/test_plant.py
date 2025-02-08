"""Unit tests for the PlantHexagon class."""

import unittest
import math
import pygame
from src.hexagons.plant import PlantHexagon
from tests.test_config import MOCK_CELL_SIZE, MOCK_COLORS


class TestPlantHexagon(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        pygame.init()
        self.screen = pygame.Surface((100, 100))
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
        # Test at t=0
        self.plant.t = 0
        self.plant.phase = 0  # Force phase to 0 for predictable testing
        self.plant.draw(self.screen)
        
        # Test at t=pi/2 (should be more green)
        self.plant.t = math.pi/2
        self.plant.draw(self.screen)
        
        # Test at t=pi (should be back to middle)
        self.plant.t = math.pi
        self.plant.draw(self.screen)

    def tearDown(self):
        """Clean up after each test method."""
        pygame.quit()


if __name__ == '__main__':
    unittest.main() 