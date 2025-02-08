"""Base renderer interface for the life simulation.

This module defines the base interface for rendering hexagonal cells and grids.
Different rendering implementations (e.g., Pygame, OpenGL) should implement this interface.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Protocol


class Renderable(Protocol):
    """Protocol defining what a renderable object must provide."""
    @property
    def points(self) -> List[Tuple[float, float]]:
        """Get the points that define the shape."""
        ...

    @property
    def color(self) -> Tuple[int, int, int]:
        """Get the current color of the object."""
        ...


class BaseRenderer(ABC):
    """Abstract base class for renderers.
    
    This class defines the interface that all renderers must implement.
    It provides methods for rendering individual hexagons and grids of hexagons.
    """
    
    @abstractmethod
    def setup(self, width: int, height: int) -> None:
        """Set up the renderer with the given dimensions.
        
        Args:
            width (int): Width of the rendering surface
            height (int): Height of the rendering surface
        """
        pass
    
    @abstractmethod
    def begin_frame(self) -> None:
        """Prepare for rendering a new frame."""
        pass
    
    @abstractmethod
    def end_frame(self) -> None:
        """Finish rendering the current frame."""
        pass
    
    @abstractmethod
    def draw_hexagon(self, hexagon: Renderable, show_grid: bool = True) -> None:
        """Draw a single hexagon.
        
        Args:
            hexagon (Renderable): The hexagon to draw
            show_grid (bool, optional): Whether to show grid lines. Defaults to True.
        """
        pass
    
    @abstractmethod
    def draw_text(self, text: str, position: Tuple[int, int], color: Tuple[int, int, int], 
                 centered: bool = False, font_size: int = 36) -> None:
        """Draw text on the screen.
        
        Args:
            text (str): The text to draw
            position (Tuple[int, int]): Position (x, y) to draw the text
            color (Tuple[int, int, int]): RGB color of the text
            centered (bool, optional): Whether to center the text at the position. Defaults to False.
            font_size (int, optional): Size of the font. Defaults to 36.
        """
        pass
    
    @abstractmethod
    def draw_overlay(self, color: Tuple[int, int, int, int]) -> None:
        """Draw a semi-transparent overlay.
        
        Args:
            color (Tuple[int, int, int, int]): RGBA color of the overlay
        """
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Clean up any resources used by the renderer."""
        pass 