"""Main entry point for the Life Simulation."""

import pygame
import sys
from src.mesh.hex_mesh import HexMesh
from src.game_state import GameStateManager
from src.renderers.pygame_renderer import PygameRenderer
from src.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    GRID_COLUMNS,
    GRID_ROWS
)


def main():
    """Run the main game loop."""
    # Initialize components
    clock = pygame.time.Clock()
    renderer = PygameRenderer()
    renderer.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
    pygame.display.set_caption('Life Simulation')

    # Create game components
    mesh = HexMesh(GRID_COLUMNS, GRID_ROWS, SCREEN_WIDTH, SCREEN_HEIGHT)
    state_manager = GameStateManager()
    
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Let state manager handle its events
            elif state_manager.handle_input(event):
                running = False  # Quit if state manager returns True
        
        # Update game state if not paused
        current_time = pygame.time.get_ticks() / 1000.0
        if state_manager.current_state == state_manager.current_state.RUNNING:
            mesh.update(current_time * state_manager.simulation_speed)
        
        # Draw everything
        renderer.begin_frame()
        
        # Draw all hexagons
        for hexagon in mesh.hexagons:
            renderer.draw_hexagon(hexagon, show_grid=state_manager.show_grid)
        
        # Draw state overlays
        if state_manager.current_state in [state_manager.current_state.PAUSED, state_manager.current_state.HELP]:
            renderer.draw_overlay((0, 0, 0, 128))
            
            if state_manager.current_state == state_manager.current_state.PAUSED:
                renderer.draw_text("PAUSED", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 
                                (255, 255, 255), centered=True)
                renderer.draw_text("Press H for help", 
                                (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30),
                                (200, 200, 200), centered=True, font_size=24)
            
            elif state_manager.current_state == state_manager.current_state.HELP:
                renderer.draw_text("CONTROLS", (SCREEN_WIDTH // 2, 50), 
                                (255, 255, 255), centered=True)
                
                y_pos = 100
                for key, description in state_manager.controls:
                    renderer.draw_text(key, (SCREEN_WIDTH // 2 - 10, y_pos),
                                    (255, 255, 0), centered=False, font_size=24)
                    renderer.draw_text(description, (SCREEN_WIDTH // 2 + 10, y_pos),
                                    (255, 255, 255), centered=False, font_size=24)
                    y_pos += 30
        
        # Always draw these overlays unless in help
        if state_manager.current_state != state_manager.current_state.HELP:
            renderer.draw_text(f"Speed: {state_manager.simulation_speed:.1f}x",
                            (10, 10), (255, 255, 255))
            renderer.draw_text(f"Grid: {'ON' if state_manager.show_grid else 'OFF'}",
                            (10, 50), (255, 255, 255))
        
        renderer.end_frame()
        clock.tick(FPS)
    
    renderer.cleanup()
    sys.exit()


if __name__ == '__main__':
    main() 