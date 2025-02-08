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
        font (pygame.font.Font): Font for rendering text overlays
        controls (List[Tuple[str, str]]): List of control descriptions
    """
    
    def __init__(self):
        """Initialize the game state manager."""
        self.current_state = GameState.RUNNING
        self.simulation_speed = 1.0
        self.show_grid = True
        # Initialize font for overlays
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
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
                
    def draw_overlay(self, screen: pygame.Surface):
        """Draw state-specific overlays on the screen.
        
        Args:
            screen (pygame.Surface): Surface to draw on
        """
        if self.current_state in [GameState.PAUSED, GameState.HELP]:
            # Draw semi-transparent overlay
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            pygame.draw.rect(overlay, (0, 0, 0, 128), overlay.get_rect())
            screen.blit(overlay, (0, 0))
            
            if self.current_state == GameState.PAUSED:
                # Draw "PAUSED" text
                text = self.font.render("PAUSED", True, (255, 255, 255))
                text_rect = text.get_rect(center=screen.get_rect().center)
                screen.blit(text, text_rect)
                
                # Draw "Press H for help" below pause text
                help_text = self.small_font.render("Press H for help", True, (200, 200, 200))
                help_rect = help_text.get_rect(midtop=(text_rect.centerx, text_rect.bottom + 10))
                screen.blit(help_text, help_rect)
            
            elif self.current_state == GameState.HELP:
                # Draw "CONTROLS" header
                header = self.font.render("CONTROLS", True, (255, 255, 255))
                header_rect = header.get_rect(midtop=(screen.get_rect().centerx, 50))
                screen.blit(header, header_rect)
                
                # Draw controls list
                y_pos = header_rect.bottom + 30
                for key, description in self.controls:
                    # Draw key
                    key_text = self.small_font.render(key, True, (255, 255, 0))
                    key_rect = key_text.get_rect(topright=(screen.get_rect().centerx - 10, y_pos))
                    screen.blit(key_text, key_rect)
                    
                    # Draw description
                    desc_text = self.small_font.render(description, True, (255, 255, 255))
                    desc_rect = desc_text.get_rect(topleft=(screen.get_rect().centerx + 10, y_pos))
                    screen.blit(desc_text, desc_rect)
                    
                    y_pos += 30
            
        # Always draw these overlays
        if self.current_state != GameState.HELP:  # Don't show during help screen
            # Draw speed indicator
            speed_text = self.font.render(f"Speed: {self.simulation_speed:.1f}x", True, (255, 255, 255))
            screen.blit(speed_text, (10, 10))
            
            # Draw grid status
            grid_text = self.font.render(f"Grid: {'ON' if self.show_grid else 'OFF'}", True, (255, 255, 255))
            screen.blit(grid_text, (10, 50)) 