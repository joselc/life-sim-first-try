"""Game state management for the Life Simulation."""

from enum import Enum, auto
import pygame


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
        
        # Define controls list
        self.controls = [
            ("P", "Pause/Resume simulation"),
            ("G", "Toggle grid lines"),
            ("+/-", "Adjust simulation speed"),
            ("H", "Show/Hide this help"),
            ("ESC", "Exit help/pause"),
            ("Q", "Quit game")
        ]
        
    def toggle_pause(self):
        """Toggle between RUNNING and PAUSED states."""
        if self.current_state == GameState.RUNNING:
            self.current_state = GameState.PAUSED
        elif self.current_state == GameState.PAUSED:
            self.current_state = GameState.RUNNING
            
    def toggle_help(self):
        """Toggle help overlay."""
        if self.current_state == GameState.HELP:
            self.current_state = GameState.RUNNING
        else:
            self.current_state = GameState.HELP
            
    def adjust_speed(self, delta: float):
        """Adjust the simulation speed.
        
        Args:
            delta (float): Amount to adjust speed by (positive or negative)
        """
        self.simulation_speed = max(0.1, min(5.0, self.simulation_speed + delta))
        
    def toggle_grid(self):
        """Toggle grid lines visibility."""
        self.show_grid = not self.show_grid
        
    def handle_input(self, event: pygame.event.Event) -> bool:
        """Handle input events for game state changes.
        
        Args:
            event (pygame.event.Event): The event to handle
            
        Returns:
            bool: True if the game should quit, False otherwise
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:  # Q key for quit
                return True
            elif event.key == pygame.K_h:  # H key for help
                self.toggle_help()
            elif event.key == pygame.K_ESCAPE:  # ESC key to exit help/pause
                if self.current_state in [GameState.HELP, GameState.PAUSED]:
                    self.current_state = GameState.RUNNING
            elif self.current_state != GameState.HELP:  # Only handle these if not in help
                if event.key == pygame.K_p:  # P key for pause
                    self.toggle_pause()
                elif event.key == pygame.K_g:  # G key for grid toggle
                    self.toggle_grid()
                elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    self.adjust_speed(0.1)  # Speed up
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    self.adjust_speed(-0.1)  # Slow down
        return False 