"""Game state management for the Life Simulation."""

from enum import Enum, auto
import pygame
from typing import List, Tuple
from . import i18n
from .i18n.language_manager import Language


class GameState(Enum):
    """Possible states of the game."""
    MENU = auto()
    RUNNING = auto()
    PAUSED = auto()
    HELP = auto()  # New state for showing controls


class GameStateManager:
    """Manages the game state and related functionality.
    
    This class handles state transitions, pause/resume functionality,
    and maintains game settings.
    
    Attributes:
        current_state (GameState): Current state of the game
        simulation_speed (float): Speed multiplier for the simulation
        show_grid (bool): Whether to show grid lines
        controls (List[Tuple[str, str]]): List of control descriptions
    """
    
    def __init__(self):
        """Initialize the game state manager."""
        self.current_state = GameState.RUNNING
        self.simulation_speed = 1.0
        self.show_grid = True
        self._update_controls()
        
    def _update_controls(self):
        """Update the controls list with current language strings."""
        self.controls: List[Tuple[str, str]] = [
            ('P', i18n.get_string('controls.pause')),
            ('H', i18n.get_string('controls.help')),
            ('G', i18n.get_string('controls.grid')),
            ('+/-', i18n.get_string('controls.speed')),
            ('ESC', i18n.get_string('controls.escape')),
            ('L', i18n.get_string('controls.language')),
            ('Q', i18n.get_string('controls.quit')),
        ]
        
    def toggle_pause(self) -> None:
        """Toggle between RUNNING and PAUSED states."""
        if self.current_state == GameState.RUNNING:
            self.current_state = GameState.PAUSED
        elif self.current_state == GameState.PAUSED:
            self.current_state = GameState.RUNNING
            
    def toggle_help(self) -> None:
        """Toggle help overlay."""
        if self.current_state == GameState.HELP:
            self.current_state = GameState.RUNNING
        else:
            self.current_state = GameState.HELP
            
    def adjust_speed(self, delta: float) -> None:
        """Adjust the simulation speed.
        
        Args:
            delta (float): Amount to adjust speed by (positive or negative)
        """
        self.simulation_speed = max(0.1, min(5.0, self.simulation_speed + delta))
        
    def toggle_grid(self) -> None:
        """Toggle grid lines visibility."""
        self.show_grid = not self.show_grid
        
    def toggle_language(self) -> None:
        """Toggle between available languages."""
        current = i18n.get_current_language()
        languages = i18n.get_available_languages()
        # Find next language in the list
        current_index = languages.index(current)
        next_index = (current_index + 1) % len(languages)
        i18n.switch_language(languages[next_index])
        # Update controls with new language
        self._update_controls()
        
    def handle_input(self, event: pygame.event.Event) -> bool:
        """Handle input events for game state changes.
        
        Args:
            event (pygame.event.Event): The event to handle
            
        Returns:
            bool: True if the game should quit, False otherwise
        """
        if event.type != pygame.KEYDOWN:
            return False

        # Always handle quit key regardless of state
        if event.key == pygame.K_q:
            return True

        # Handle help toggle with H key in any state
        if event.key == pygame.K_h:
            self.toggle_help()
            return False

        # Handle language toggle with L key in any state
        if event.key == pygame.K_l:
            self.toggle_language()
            return False

        # Handle escape key in help or paused state
        if event.key == pygame.K_ESCAPE:
            if self.current_state in [GameState.HELP, GameState.PAUSED]:
                self.current_state = GameState.RUNNING
            return False

        # Only handle these keys if not in help state
        if self.current_state != GameState.HELP:
            if event.key == pygame.K_p:
                self.toggle_pause()
            elif event.key == pygame.K_g:
                self.toggle_grid()
            elif event.key in [pygame.K_PLUS, pygame.K_KP_PLUS]:
                self.adjust_speed(0.1)
            elif event.key in [pygame.K_MINUS, pygame.K_KP_MINUS]:
                self.adjust_speed(-0.1)

        return False 