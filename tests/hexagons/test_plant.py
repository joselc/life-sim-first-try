"""Unit tests for the PlantHexagon class."""

import unittest
from unittest.mock import Mock, patch
from src.hexagons.plant import PlantHexagon
from src.hexagons.plant_states import PlantState
from tests.test_config import MOCK_CELL_SIZE, MOCK_COLORS
import math


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
            PlantState.FLOWERING: MOCK_COLORS['MATURE'],  # Should keep mature color as background
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
            PlantState.FLOWERING: MOCK_COLORS['FLOWER'],  # Red color for flower dots
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
            PlantState.FLOWERING: self.plant.FLOWER_DOT_RADIUS,
            PlantState.MATURE: 0.0,
            PlantState.DYING: 0.0,
            PlantState.DEAD: 0.0
        }

        for state, expected_radius in state_radius_map.items():
            mock_state_manager.state = state
            self.assertEqual(self.plant.detail_radius, expected_radius)

    def test_flower_animation_initialization(self):
        """Test that flower animation is properly initialized."""
        self.assertEqual(self.plant.animation_time, 0.0)
        self.assertFalse(hasattr(self.plant, 'flower_angle'))  # Should not exist until flowering

    def test_flower_animation_update(self):
        """Test that flower animation updates correctly during flowering state."""
        # Set plant to flowering state
        mock_state_manager = Mock()
        mock_state_manager.state = PlantState.FLOWERING
        self.plant.state_manager = mock_state_manager

        # Test animation after one update
        dt = 0.1
        self.plant.update(dt)
        self.assertEqual(self.plant.animation_time, dt)
        
        # Check that flower_angle is calculated correctly
        expected_angle = math.sin(dt * self.plant.FLOWER_SWAY_SPEED * 2 * math.pi) * self.plant.FLOWER_SWAY_ANGLE
        self.assertAlmostEqual(self.plant.flower_angle, expected_angle)

        # Test animation accumulates time correctly
        self.plant.update(dt)
        self.assertEqual(self.plant.animation_time, dt * 2)

    def test_flower_animation_bounds(self):
        """Test that flower animation stays within expected bounds."""
        mock_state_manager = Mock()
        mock_state_manager.state = PlantState.FLOWERING
        self.plant.state_manager = mock_state_manager

        # Test multiple updates to verify bounds
        for _ in range(50):  # Test over multiple frames
            self.plant.update(0.1)
            # Angle should never exceed maximum sway angle
            self.assertLessEqual(abs(self.plant.flower_angle), self.plant.FLOWER_SWAY_ANGLE)

    def test_animation_state_specific(self):
        """Test that animation only updates during flowering state."""
        # Test in non-flowering state
        mock_state_manager = Mock()
        mock_state_manager.state = PlantState.MATURE
        self.plant.state_manager = mock_state_manager

        self.plant.update(0.1)
        self.assertEqual(self.plant.animation_time, 0.0)  # Should not accumulate time
        self.assertFalse(hasattr(self.plant, 'flower_angle'))  # Should not have angle

        # Switch to flowering
        mock_state_manager.state = PlantState.FLOWERING
        self.plant.update(0.1)
        self.assertGreater(self.plant.animation_time, 0.0)  # Should now accumulate time
        self.assertTrue(hasattr(self.plant, 'flower_angle'))  # Should now have angle


if __name__ == '__main__':
    unittest.main() 