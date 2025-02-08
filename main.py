import pygame
import sys
from src.mesh.hex_mesh import HexMesh
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

    # Create a HexMesh instance that computes the mesh
    mesh = HexMesh(GRID_COLUMNS, GRID_ROWS, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update mesh evolution with current time (in seconds)
        mesh.update(pygame.time.get_ticks() / 1000.0)
        
        # Fill the screen with a color
        screen.fill(BACKGROUND_COLOR)
        
        # Draw the evolving hexagon mesh from HexMesh
        mesh.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main() 