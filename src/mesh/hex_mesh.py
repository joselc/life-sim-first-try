import math
import random
import pygame
from ..hexagons.plant import PlantHexagon
from ..hexagons.ground import GroundHexagon


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
                
                # Randomly choose between a plant hexagon and ground hexagon
                if random.random() < 0.5:
                    hexagon = PlantHexagon(cx, cy, a)
                else:
                    hexagon = GroundHexagon(cx, cy, a)
                
                self.hexagons.append(hexagon)

    def update(self, t):
        for hexagon in self.hexagons:
            hexagon.update(t)

    def draw(self, screen):
        for hexagon in self.hexagons:
            hexagon.draw(screen) 