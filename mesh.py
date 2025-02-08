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
                # Assign a random phase for evolution
                phase = random.uniform(0, 2 * math.pi)
                self.hexagons.append((points, phase))

    def update(self, t):
        self.t = t

    def draw(self, screen):
        # Use current time, default 0 if not updated yet
        current_time = getattr(self, 't', 0)
        # Define base colors: brown and green
        green = (34, 139, 34)
        brown = (139, 69, 19)
        
        for points, phase in self.hexagons:
            # Compute modulation factor based on time and phase
            factor = 0.5 * (1 + math.sin(current_time + phase))
            # Interpolate between brown and green
            fill_color = ( int(brown[0]*(1 - factor) + green[0]*factor),
                           int(brown[1]*(1 - factor) + green[1]*factor),
                           int(brown[2]*(1 - factor) + green[2]*factor) )
            pygame.draw.polygon(screen, fill_color, points, 0)  # fill hexagon
            pygame.draw.polygon(screen, (200, 200, 200), points, 1)  # draw outline 