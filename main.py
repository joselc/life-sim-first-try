import pygame
import sys
from src.mesh.hex_mesh import HexMesh
from src.game_state import GameStateManager
from src.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    BACKGROUND_COLOR,
    GRID_COLUMNS,
    GRID_ROWS
)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
        screen.fill(BACKGROUND_COLOR)
        mesh.draw(screen, show_grid=state_manager.show_grid)
        state_manager.draw_overlay(screen)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main() 