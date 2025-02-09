"""Unit tests for the PlantHexagon class."""

import unittest
from unittest.mock import Mock, patch
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
        # Only verify that a state manager exists, not its internal state
        self.assertIsNotNone(self.plant.state_manager)

    def test_update_delegates_to_state_manager(self):
        """Test that update properly delegates to the state manager."""
        # Create a mock state manager
        mock_state_manager = Mock()
        self.plant.state_manager = mock_state_manager

        # Call update
        self.plant.update(0.1)

        # Verify the state manager's update was called with correct time
        mock_state_manager.update.assert_called_once_with(0.1)

    def test_base_color_mapping(self):
        """Test that base colors are correctly mapped to states."""
        # Create a mock state manager
        mock_state_manager = Mock()
        self.plant.state_manager = mock_state_manager

        # Test each state
        state_color_map = {
            PlantState.SEED: MOCK_COLORS['BROWN'],
            PlantState.GROWING: MOCK_COLORS['BROWN'],
            PlantState.MATURE: MOCK_COLORS['MATURE'],
            PlantState.DYING: MOCK_COLORS['DYING'],
            PlantState.DEAD: MOCK_COLORS['DEAD']
        }

        for state, expected_color in state_color_map.items():
            mock_state_manager.state = state
            self.assertEqual(self.plant.base_color, expected_color)

    def test_detail_color_mapping(self):
        """Test that detail colors are correctly mapped to states."""
        # Create a mock state manager
        mock_state_manager = Mock()
        self.plant.state_manager = mock_state_manager

        # Test each state
        state_color_map = {
            PlantState.SEED: MOCK_COLORS['YELLOW'],
            PlantState.GROWING: MOCK_COLORS['GROWING'],
            PlantState.MATURE: (0, 0, 0),  # Black (invisible)
            PlantState.DYING: (0, 0, 0),   # Black (invisible)
            PlantState.DEAD: (0, 0, 0)     # Black (invisible)
        }

        for state, expected_color in state_color_map.items():
            mock_state_manager.state = state
            self.assertEqual(self.plant.detail_color, expected_color)

    def test_detail_radius_mapping(self):
        """Test that detail radius is correctly mapped to states."""
        # Create a mock state manager
        mock_state_manager = Mock()
        self.plant.state_manager = mock_state_manager

        # Test each state
        state_radius_map = {
            PlantState.SEED: self.plant.SEED_DOT_RADIUS,
            PlantState.GROWING: self.plant.GROWING_DOT_RADIUS,
            PlantState.MATURE: 0.0,
            PlantState.DYING: 0.0,
            PlantState.DEAD: 0.0
        }

        for state, expected_radius in state_radius_map.items():
            mock_state_manager.state = state
            self.assertEqual(self.plant.detail_radius, expected_radius)


if __name__ == '__main__':
    unittest.main() 