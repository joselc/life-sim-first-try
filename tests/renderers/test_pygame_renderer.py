"""Tests for the Pygame renderer implementation."""

import unittest
import pygame
import math
from unittest.mock import Mock, patch
from src.renderers.pygame_renderer import PygameRenderer
from src.hexagons.plant_states import PlantState
from tests.renderers.test_base import MockRenderable
from tests.test_config import (
    MOCK_SCREEN_WIDTH,
    MOCK_SCREEN_HEIGHT,
    MOCK_COLORS
)


class MockFloweringPlant(MockRenderable):
    """Mock implementation of a flowering plant for testing."""
    
    def __init__(self, cx, cy, a, flower_angle=0.0):
        super().__init__(
            points=[(0, 0), (10, 0), (10, 10), (0, 10)],
            color=MOCK_COLORS['FLOWER'],
            base_color=MOCK_COLORS['MATURE']
        )
        self.cx = cx
        self.cy = cy
        self.a = a
        self.flower_angle = flower_angle
        self.FLOWER_ORBIT_RADIUS = 0.4
        self.detail_color = MOCK_COLORS['FLOWER']
        self.detail_radius = 0.12
        self.state_manager = Mock()
        self.state_manager.state = PlantState.FLOWERING


class TestPygameRenderer(unittest.TestCase):
    """Test cases for the Pygame renderer."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.renderer = PygameRenderer()
        self.renderer.setup(MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT)
        # Create a mock renderable with both color and base_color
        self.renderable = MockRenderable(
            points=[(0, 0), (10, 0), (10, 10), (0, 10)],
            color=MOCK_COLORS['GREEN'],
            base_color=MOCK_COLORS['GREEN']  # Add base_color
        )

    def test_initialization(self):
        """Test that renderer is initialized correctly."""
        self.assertIsNotNone(self.renderer.screen)
        self.assertIsNotNone(self.renderer.font)
        self.assertIsNotNone(self.renderer.small_font)
        self.assertEqual(self.renderer.screen.get_width(), MOCK_SCREEN_WIDTH)
        self.assertEqual(self.renderer.screen.get_height(), MOCK_SCREEN_HEIGHT)

    def test_begin_frame(self):
        """Test that begin_frame clears the screen."""
        self.renderer.begin_frame()
        # Check that screen is filled with background color
        color = self.renderer.screen.get_at((0, 0))[:3]  # Get RGB values
        self.assertEqual(color, (30, 30, 30))  # Background color

    def test_draw_hexagon(self):
        """Test that hexagons are drawn correctly."""
        self.renderer.begin_frame()
        self.renderer.draw_hexagon(self.renderable, show_grid=True)
        
        # Check that the hexagon was drawn with the correct color
        # Test a point inside the hexagon (5, 5)
        color = self.renderer.screen.get_at((5, 5))[:3]  # Get RGB values
        self.assertEqual(color, self.renderable.base_color)

    def test_draw_text(self):
        """Test that text is drawn correctly."""
        text = "Test"
        color = (255, 255, 255)
        position = (50, 50)  # Move position to ensure it's within bounds
        
        self.renderer.begin_frame()
        self.renderer.draw_text(text, position, color)
        
        # Get the color of a few pixels around the text position
        colors = [
            self.renderer.screen.get_at((x, y))[:3]
            for x in range(position[0]-5, position[0]+5)
            for y in range(position[1]-5, position[1]+5)
        ]
        
        # At least one pixel should be different from background
        background_color = (30, 30, 30)
        self.assertTrue(any(c != background_color for c in colors),
                       "No text pixels found different from background")

    def test_draw_overlay(self):
        """Test that overlay is drawn correctly."""
        overlay_color = (0, 0, 0, 128)
        
        self.renderer.begin_frame()
        self.renderer.draw_overlay(overlay_color)
        
        # Check that the overlay was drawn
        color = self.renderer.screen.get_at((0, 0))
        self.assertNotEqual(color[:3], (30, 30, 30))  # Should not be background color

    def test_cleanup(self):
        """Test that cleanup works without errors."""
        try:
            self.renderer.cleanup()
            success = True
        except Exception:
            success = False
        self.assertTrue(success)

    def test_flower_dot_positions(self):
        """Test that flower dots are positioned correctly."""
        # Create a flowering plant at the center with a known angle
        plant = MockFloweringPlant(50, 50, 10, flower_angle=0.0)
        
        # Mock pygame.draw.circle to capture the positions where circles are drawn
        drawn_positions = []
        def mock_draw_circle(screen, color, pos, radius):
            drawn_positions.append(pos)
        
        with patch('pygame.draw.circle', side_effect=mock_draw_circle):
            self.renderer.begin_frame()
            self.renderer.draw_hexagon(plant)
        
        # Should have drawn exactly 3 flower dots
        self.assertEqual(len(drawn_positions), 3)
        
        # Calculate expected positions (120 degrees apart)
        distance = plant.a * plant.FLOWER_ORBIT_RADIUS
        expected_positions = []
        for i in range(3):
            theta = plant.flower_angle + (i * 2 * math.pi / 3)
            x = int(plant.cx + distance * math.cos(theta))
            y = int(plant.cy + distance * math.sin(theta))
            expected_positions.append((x, y))
        
        # Verify each drawn position matches expected position
        for drawn, expected in zip(drawn_positions, expected_positions):
            self.assertEqual(drawn, expected)

    def test_flower_dot_angles(self):
        """Test that flower dots maintain correct angular spacing."""
        # Create a flowering plant with a non-zero angle
        test_angle = math.pi / 4  # 45 degrees
        plant = MockFloweringPlant(50, 50, 10, flower_angle=test_angle)
        
        drawn_positions = []
        def mock_draw_circle(screen, color, pos, radius):
            drawn_positions.append(pos)
        
        with patch('pygame.draw.circle', side_effect=mock_draw_circle):
            self.renderer.begin_frame()
            self.renderer.draw_hexagon(plant)
        
        # Calculate angles between consecutive dots
        angles = []
        center = (plant.cx, plant.cy)
        for i in range(3):
            pos1 = drawn_positions[i]
            pos2 = drawn_positions[(i + 1) % 3]
            
            # Calculate angles relative to center
            angle1 = math.atan2(pos1[1] - center[1], pos1[0] - center[0])
            angle2 = math.atan2(pos2[1] - center[1], pos2[0] - center[0])
            
            # Calculate angle difference and normalize to [0, 2π]
            diff = (angle2 - angle1) % (2 * math.pi)
            angles.append(diff)
        
        # All angles should be approximately 120 degrees (2π/3 radians)
        # Use places=1 to account for integer rounding effects
        expected_angle = 2 * math.pi / 3
        for angle in angles:
            self.assertAlmostEqual(angle, expected_angle, places=1)

    def test_flower_dot_distance(self):
        """Test that flower dots maintain correct distance from center."""
        plant = MockFloweringPlant(50, 50, 10)
        
        drawn_positions = []
        def mock_draw_circle(screen, color, pos, radius):
            drawn_positions.append(pos)
        
        with patch('pygame.draw.circle', side_effect=mock_draw_circle):
            self.renderer.begin_frame()
            self.renderer.draw_hexagon(plant)
        
        # Calculate expected distance
        expected_distance = plant.a * plant.FLOWER_ORBIT_RADIUS
        
        # Check that each dot is at the correct distance from center
        # Allow for integer rounding by checking if distance is within 0.5 units
        center = (plant.cx, plant.cy)
        for pos in drawn_positions:
            dx = pos[0] - center[0]
            dy = pos[1] - center[1]
            distance = math.sqrt(dx*dx + dy*dy)
            self.assertLess(abs(distance - expected_distance), 0.5,
                          f"Distance {distance} differs from expected {expected_distance} by more than 0.5 units")

    def tearDown(self):
        """Clean up after each test method."""
        pygame.quit()


if __name__ == '__main__':
    unittest.main() 