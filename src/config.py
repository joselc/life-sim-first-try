"""Configuration settings for the life simulation.

This module contains all the configurable parameters for the life simulation,
including display settings, grid dimensions, and color definitions.

Constants:
    SCREEN_WIDTH (int): Width of the game window in pixels
    SCREEN_HEIGHT (int): Height of the game window in pixels
    FPS (int): Target frames per second for the simulation
    BACKGROUND_COLOR (Tuple[int, int, int]): RGB color for the window background
    
    GRID_COLUMNS (int): Number of columns in the hexagonal grid
    GRID_ROWS (int): Number of rows in the hexagonal grid
    PLANT_SPAWN_PROBABILITY (float): Probability (0-1) of spawning a plant cell
    
    COLORS (Dict[str, Tuple[int, int, int]]): Dictionary of RGB color definitions
        for various elements in the simulation
"""

# Display settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = (30, 30, 30)

# Grid settings
GRID_COLUMNS = 80
GRID_ROWS = 60
PLANT_SPAWN_PROBABILITY = 0.5

# Colors
COLORS = {
    'GREEN': (34, 139, 34),    # Forest green for plants
    'BROWN': (139, 69, 19),    # Saddle brown for ground/soil
    'GRID_LINES': (200, 200, 200)  # Light gray for grid lines
} 