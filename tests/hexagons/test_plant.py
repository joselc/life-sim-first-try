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
        
        # Update should stay in seed state initially
        self.plant.update(0.1)
        self.assertEqual(self.plant.state_manager.state, PlantState.SEED)
        
        # After SEED_DURATION, should transition to growing
        self.plant.update(self.plant.state_manager.SEED_DURATION)
        self.assertEqual(self.plant.state_manager.state, PlantState.GROWING)
        
        # Should be growing for a while
        self.plant.update(self.plant.state_manager.GROWTH_THRESHOLD / 2)
        self.assertEqual(self.plant.state_manager.state, PlantState.GROWING)
        self.assertGreater(self.plant.state_manager.growth, 0.0)
        
        # After growth threshold, should be mature
        self.plant.update(self.plant.state_manager.GROWTH_THRESHOLD)  # Complete growth
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
        # Start as seed (should be brown with yellow dot)
        self.assertEqual(self.plant.state_manager.state, PlantState.SEED)
        self.assertEqual(self.plant.base_color, MOCK_COLORS['BROWN'])
        
        # Growing should be brown with green dot
        self.plant.update(self.plant.state_manager.SEED_DURATION + 0.1)
        self.assertEqual(self.plant.state_manager.state, PlantState.GROWING)
        self.assertEqual(self.plant.base_color, MOCK_COLORS['BROWN'])
        
        # Progress growth
        self.plant.update(self.plant.state_manager.GROWTH_THRESHOLD / 2)
        self.assertGreater(self.plant.state_manager.growth, 0.0)
        self.assertLess(self.plant.state_manager.growth, 1.0)
        
        # Mature should be solid green
        self.plant.update(self.plant.state_manager.GROWTH_THRESHOLD)  # Complete growth
        self.assertEqual(self.plant.state_manager.state, PlantState.MATURE)
        self.assertEqual(self.plant.base_color, MOCK_COLORS['MATURE'])
        
        # Start dying
        self.plant.update(self.plant.state_manager.MATURE_MAX_TIME + 0.1)
        self.assertEqual(self.plant.state_manager.state, PlantState.DYING)
        self.assertEqual(self.plant.base_color, MOCK_COLORS['DYING'])

    def assertColorCloserTo(self, color, target, other):
        """Assert that color is closer to target than to other color."""
        target_dist = sum((c1 - c2) ** 2 for c1, c2 in zip(color, target))
        other_dist = sum((c1 - c2) ** 2 for c1, c2 in zip(color, other))
        self.assertLess(target_dist, other_dist)


if __name__ == '__main__':
    unittest.main() 