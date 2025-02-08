import math
import random
import pygame


class HexMesh:
    def __init__(self, num_columns, num_rows, display_width, display_height):
        # Calculate side length 'a' so that vertical span fits display_height exactly
        a = display_height / (num_rows * math.sqrt(3))  # side length
        # Total grid width = 2*a + (num_columns - 1)*1.5*a
        grid_width = 2 * a + (num_columns - 1) * (1.5 * a)
        offset_x = (display_width - grid_width) / 2
        offset_y = 0  # even columns will touch top
        
        self.hexagons = []
        for i in range(num_columns):
            for j in range(num_rows):
                # Compute center of hexagon for column i, row j
                cx = offset_x + a + i * (1.5 * a)
                if i % 2 == 0:
                    cy = offset_y + (a * math.sqrt(3) / 2) + j * (a * math.sqrt(3))
                else:
                    cy = offset_y + a * math.sqrt(3) + j * (a * math.sqrt(3))
                
                # Compute the 6 vertices of the hexagon (flat-topped)
                points = [
                    (cx + a, cy),
                    (cx + a/2, cy + (a * math.sqrt(3) / 2)),
                    (cx - a/2, cy + (a * math.sqrt(3) / 2)),
                    (cx - a, cy),
                    (cx - a/2, cy - (a * math.sqrt(3) / 2)),
                    (cx + a/2, cy - (a * math.sqrt(3) / 2))
                ]
                # Select fill color randomly: green or brown
                fill_color = random.choice([(34, 139, 34), (139, 69, 19)])
                self.hexagons.append((points, fill_color))

    def draw(self, screen):
        for points, fill_color in self.hexagons:
            pygame.draw.polygon(screen, fill_color, points, 0)  # fill hexagon
            pygame.draw.polygon(screen, (200, 200, 200), points, 1)  # draw outline 