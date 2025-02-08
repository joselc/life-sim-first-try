"""Tests for the base renderer interface and renderable protocol."""

import unittest
from typing import List, Tuple
from src.renderers.base import Renderable, BaseRenderer


class MockRenderable:
    """Mock implementation of the Renderable protocol for testing."""
    
    def __init__(self, points: List[Tuple[float, float]], color: Tuple[int, int, int]):
        self._points = points
        self._color = color
    
    @property
    def points(self) -> List[Tuple[float, float]]:
        return self._points
    
    @property
    def color(self) -> Tuple[int, int, int]:
        return self._color


class MockRenderer(BaseRenderer):
    """Mock renderer implementation for testing."""
    
    def __init__(self):
        self.setup_called = False
        self.begin_frame_called = False
        self.end_frame_called = False
        self.cleanup_called = False
        self.drawn_hexagons = []
        self.drawn_texts = []
        self.drawn_overlays = []
    
    def setup(self, width: int, height: int) -> None:
        self.setup_called = True
        self.width = width
        self.height = height
    
    def begin_frame(self) -> None:
        self.begin_frame_called = True
    
    def end_frame(self) -> None:
        self.end_frame_called = True
    
    def draw_hexagon(self, hexagon: Renderable, show_grid: bool = True) -> None:
        self.drawn_hexagons.append((hexagon, show_grid))
    
    def draw_text(self, text: str, position: Tuple[int, int], color: Tuple[int, int, int],
                 centered: bool = False, font_size: int = 36) -> None:
        self.drawn_texts.append((text, position, color, centered, font_size))
    
    def draw_overlay(self, color: Tuple[int, int, int, int]) -> None:
        self.drawn_overlays.append(color)
    
    def cleanup(self) -> None:
        self.cleanup_called = True


class TestRenderable(unittest.TestCase):
    """Test cases for the Renderable protocol."""
    
    def setUp(self):
        self.points = [(0, 0), (1, 0), (1, 1)]
        self.color = (255, 0, 0)
        self.renderable = MockRenderable(self.points, self.color)
    
    def test_points_property(self):
        """Test that points property returns the correct points."""
        self.assertEqual(self.renderable.points, self.points)
    
    def test_color_property(self):
        """Test that color property returns the correct color."""
        self.assertEqual(self.renderable.color, self.color)


class TestBaseRenderer(unittest.TestCase):
    """Test cases for the BaseRenderer interface."""
    
    def setUp(self):
        self.renderer = MockRenderer()
        self.renderable = MockRenderable([(0, 0), (1, 1)], (255, 0, 0))
    
    def test_setup(self):
        """Test that setup method is called with correct parameters."""
        self.renderer.setup(800, 600)
        self.assertTrue(self.renderer.setup_called)
        self.assertEqual(self.renderer.width, 800)
        self.assertEqual(self.renderer.height, 600)
    
    def test_frame_methods(self):
        """Test that frame methods are called in correct order."""
        self.renderer.begin_frame()
        self.assertTrue(self.renderer.begin_frame_called)
        
        self.renderer.end_frame()
        self.assertTrue(self.renderer.end_frame_called)
    
    def test_draw_hexagon(self):
        """Test that draw_hexagon method records correct parameters."""
        self.renderer.draw_hexagon(self.renderable, show_grid=True)
        self.assertEqual(len(self.renderer.drawn_hexagons), 1)
        hexagon, show_grid = self.renderer.drawn_hexagons[0]
        self.assertEqual(hexagon, self.renderable)
        self.assertTrue(show_grid)
    
    def test_draw_text(self):
        """Test that draw_text method records correct parameters."""
        text = "Test"
        position = (10, 20)
        color = (255, 255, 255)
        self.renderer.draw_text(text, position, color, centered=True, font_size=24)
        self.assertEqual(len(self.renderer.drawn_texts), 1)
        drawn = self.renderer.drawn_texts[0]
        self.assertEqual(drawn, (text, position, color, True, 24))
    
    def test_draw_overlay(self):
        """Test that draw_overlay method records correct parameters."""
        color = (0, 0, 0, 128)
        self.renderer.draw_overlay(color)
        self.assertEqual(len(self.renderer.drawn_overlays), 1)
        self.assertEqual(self.renderer.drawn_overlays[0], color)
    
    def test_cleanup(self):
        """Test that cleanup method is called."""
        self.renderer.cleanup()
        self.assertTrue(self.renderer.cleanup_called)


if __name__ == '__main__':
    unittest.main() 