"""Pygame-specific implementation of the renderer interface."""

import pygame
from typing import Tuple
from .base import BaseRenderer, Renderable
from ..config import COLORS


class PygameRenderer(BaseRenderer):
    """Pygame implementation of the renderer interface."""
    
    def __init__(self):
        """Initialize the Pygame renderer."""
        self.screen = None
        self.font = None
        self.small_font = None
    
    def setup(self, width: int, height: int) -> None:
        """Set up the Pygame renderer.
        
        Args:
            width (int): Width of the rendering surface
            height (int): Height of the rendering surface
        """
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def begin_frame(self) -> None:
        """Clear the screen and prepare for rendering."""
        self.screen.fill((30, 30, 30))  # Background color
    
    def end_frame(self) -> None:
        """Update the display."""
        pygame.display.flip()
    
    def draw_hexagon(self, hexagon: Renderable, show_grid: bool = True) -> None:
        """Draw a hexagon using Pygame.
        
        Args:
            hexagon (Renderable): The hexagon to draw
            show_grid (bool, optional): Whether to show grid lines. Defaults to True.
        """
        # Draw the base hexagon
        pygame.draw.polygon(self.screen, hexagon.base_color, hexagon.points, 0)
        
        # Draw any additional details
        if hasattr(hexagon, 'detail_color') and hasattr(hexagon, 'detail_radius'):
            center = (int(hexagon.cx), int(hexagon.cy))
            radius = int(hexagon.a * hexagon.detail_radius)
            if radius > 0:
                pygame.draw.circle(self.screen, hexagon.detail_color, center, radius)
        
        # Draw the grid lines if enabled
        if show_grid:
            pygame.draw.polygon(self.screen, COLORS['GRID_LINES'], hexagon.points, 1)
    
    def draw_text(self, text: str, position: Tuple[int, int], color: Tuple[int, int, int],
                 centered: bool = False, font_size: int = 36) -> None:
        """Draw text using Pygame.
        
        Args:
            text (str): The text to draw
            position (Tuple[int, int]): Position to draw the text
            color (Tuple[int, int, int]): RGB color of the text
            centered (bool, optional): Whether to center the text. Defaults to False.
            font_size (int, optional): Size of the font. Defaults to 36.
        """
        font = self.font if font_size >= 36 else self.small_font
        text_surface = font.render(text, True, color)
        if centered:
            text_rect = text_surface.get_rect(center=position)
        else:
            text_rect = text_surface.get_rect(topleft=position)
        self.screen.blit(text_surface, text_rect)
    
    def draw_overlay(self, color: Tuple[int, int, int, int]) -> None:
        """Draw a semi-transparent overlay using Pygame.
        
        Args:
            color (Tuple[int, int, int, int]): RGBA color of the overlay
        """
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(overlay, color, overlay.get_rect())
        self.screen.blit(overlay, (0, 0))
    
    def cleanup(self) -> None:
        """Clean up Pygame resources."""
        pygame.quit() 