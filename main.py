import pygame
import sys
from mesh import HexMesh


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Simple Pygame Base Project')

    # Create a HexMesh instance that computes the mesh
    mesh = HexMesh(80, 60, 800, 600)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update mesh evolution with current time (in seconds)
        mesh.update(pygame.time.get_ticks() / 1000.0)
        
        # Fill the screen with a color
        screen.fill((30, 30, 30))
        
        # Draw the evolving hexagon mesh from HexMesh
        mesh.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main() 