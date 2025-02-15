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
    SEED_SURVIVAL_THRESHOLD (float): Default probability (0-1) of a seed surviving
    PLANT_FLOWERING_PROBABILITY (float): Probability (0-1) of a plant flowering
    WATER_SPAWN_PROBABILITY (float): Probability (0-1) of initial water hexagon for group formation
    MAX_WATER_PERCENTAGE (float): Maximum percentage of map can be water
    
    COLORS (Dict[str, Tuple[int, int, int]]): Dictionary of RGB color definitions
        for various elements in the simulation
"""

# Display settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = (30, 30, 30)

# Grid settings
GRID_COLUMNS = 16
GRID_ROWS = 12
PLANT_SPAWN_PROBABILITY = 0.5
SEED_SURVIVAL_THRESHOLD = 0.7  # 70% chance of survival by default
PLANT_FLOWERING_PROBABILITY = 0.3  # 30% chance of flowering by default
WATER_SPAWN_PROBABILITY = 0.2  # 20% chance of initial water hexagon for group formation
MAX_WATER_PERCENTAGE = 0.3  # Maximum 30% of map can be water

# Colors
COLORS = {
    'GREEN': (34, 139, 34),      # Forest green for mature plants
    'BROWN': (139, 69, 19),      # Saddle brown for ground/soil
    'GRID_LINES': (200, 200, 200),  # Light gray for grid lines
    'SEED': (101, 67, 33),       # Dark brown for seeds
    'GROWING': (154, 205, 50),   # Yellow-green for growing plants
    'MATURE': (34, 139, 34),     # Forest green for mature plants
    'DYING': (205, 133, 63),     # Peru brown for dying plants
    'DEAD': (139, 69, 19),       # Same as ground color
    'YELLOW': (255, 215, 0),     # Gold color for seed dots
    'FLOWER': (255, 0, 0),       # Red color for flower dots
    'WATER': (0, 105, 148)       # Deep blue for water
} 