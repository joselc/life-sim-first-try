"""Unit tests for the PlantHexagon class."""

import unittest
from src.hexagons.plant import PlantHexagon
from src.hexagons.plant_states import PlantState
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
        self.assertEqual(self.plant.state_manager.state, PlantState.SEED)
        self.assertEqual(self.plant.state_manager.time_in_state, 0.0)
        self.assertEqual(self.plant.state_manager.health, 1.0)
        self.assertEqual(self.plant.state_manager.growth, 0.0)

    def test_lifecycle(self):
        """Test that plant goes through its lifecycle states correctly."""
        # Start as seed
        self.assertEqual(self.plant.state_manager.state, PlantState.SEED)
        
        # Update should transition to growing immediately
        self.plant.update(0.1)
        self.assertEqual(self.plant.state_manager.state, PlantState.GROWING)
        
        # Should be growing for a while
        self.plant.update(0.5)
        self.assertEqual(self.plant.state_manager.state, PlantState.GROWING)
        self.assertGreater(self.plant.state_manager.growth, 0.0)
        
        # After growth threshold, should be mature
        self.plant.update(0.5)  # Complete growth
        self.assertEqual(self.plant.state_manager.state, PlantState.MATURE)
        
        # Should stay mature for a while
        self.plant.update(self.plant.state_manager.MATURE_MAX_TIME - 0.1)
        self.assertEqual(self.plant.state_manager.state, PlantState.MATURE)
        
        # Eventually should start dying
        self.plant.update(0.2)  # Push over max time
        self.assertEqual(self.plant.state_manager.state, PlantState.DYING)
        
        # Finally should die
        self.plant.update(self.plant.state_manager.DYING_DURATION)
        self.assertEqual(self.plant.state_manager.state, PlantState.DEAD)

    def test_color_transitions(self):
        """Test that color changes appropriately with state transitions."""
        green = MOCK_COLORS['GREEN']
        brown = MOCK_COLORS['BROWN']
        
        # Start as seed (should be brown)
        self.assertEqual(self.plant.state_manager.state, PlantState.SEED)
        self.assertEqual(self.plant.state_manager.color_factor, 0.0)
        
        # Growing should transition towards green
        self.plant.update(0.1)  # Start growing
        self.plant.update(0.5)  # Progress growth
        self.assertEqual(self.plant.state_manager.state, PlantState.GROWING)
        self.assertGreater(self.plant.state_manager.growth, 0.0)
        self.assertLess(self.plant.state_manager.growth, 1.0)
        
        # Mature should be most green
        self.plant.update(0.5)  # Complete growth
        self.assertEqual(self.plant.state_manager.state, PlantState.MATURE)
        self.assertEqual(self.plant.state_manager.color_factor, 1.0)
        
        # Dying should transition back to brown
        self.plant.update(self.plant.state_manager.MATURE_MAX_TIME + 0.1)  # Start dying
        self.plant.update(self.plant.state_manager.DYING_DURATION / 2)  # Half dead
        self.assertEqual(self.plant.state_manager.state, PlantState.DYING)
        self.assertLess(self.plant.state_manager.color_factor, 1.0)

    def assertColorCloserTo(self, color, target, other):
        """Assert that color is closer to target than to other color."""
        target_dist = sum((c1 - c2) ** 2 for c1, c2 in zip(color, target))
        other_dist = sum((c1 - c2) ** 2 for c1, c2 in zip(color, other))
        self.assertLess(target_dist, other_dist)


if __name__ == '__main__':
    unittest.main() 