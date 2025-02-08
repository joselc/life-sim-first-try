"""Tests for the Pygame renderer implementation."""

import unittest
import pygame
from src.renderers.pygame_renderer import PygameRenderer
from tests.renderers.test_base import MockRenderable
from tests.test_config import (
    MOCK_SCREEN_WIDTH,
    MOCK_SCREEN_HEIGHT,
    MOCK_COLORS
)


class TestPygameRenderer(unittest.TestCase):
    """Test cases for the Pygame renderer."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.renderer = PygameRenderer()
        self.renderer.setup(MOCK_SCREEN_WIDTH, MOCK_SCREEN_HEIGHT)
        self.renderable = MockRenderable(
            points=[(0, 0), (10, 0), (10, 10), (0, 10)],
            color=MOCK_COLORS['GREEN']
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
        color = self.renderer.screen.get_at((5, 5))[:3]  # Get RGB values
        self.assertEqual(color, self.renderable.color)

    def test_draw_text(self):
        """Test that text is drawn correctly."""
        text = "Test"
        color = (255, 255, 255)
        position = (10, 10)
        
        self.renderer.begin_frame()
        self.renderer.draw_text(text, position, color)
        
        # Check that something was drawn at the text position
        drawn_color = self.renderer.screen.get_at(position)[:3]
        self.assertNotEqual(drawn_color, (30, 30, 30))  # Should not be background color

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

    def tearDown(self):
        """Clean up after each test method."""
        pygame.quit()


if __name__ == '__main__':
    unittest.main() 