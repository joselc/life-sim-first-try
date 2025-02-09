"""Test configuration with mock values for testing."""

# Mock display settings
MOCK_SCREEN_WIDTH = 100
MOCK_SCREEN_HEIGHT = 100
MOCK_CELL_SIZE = 10

# Mock grid settings
MOCK_COLUMNS = 3
MOCK_ROWS = 3

# Mock colors for testing (matching the actual colors from src/config.py)
MOCK_COLORS = {
    'GREEN': (34, 139, 34),      # Forest green for mature plants
    'BROWN': (139, 69, 19),      # Saddle brown for ground/soil
    'GRID_LINES': (200, 200, 200),  # Light gray for grid lines
    'SEED': (101, 67, 33),       # Dark brown for seeds
    'GROWING': (154, 205, 50),   # Yellow-green for growing plants
    'MATURE': (34, 139, 34),     # Forest green for mature plants
    'DYING': (205, 133, 63),     # Peru brown for dying plants
    'DEAD': (139, 69, 19),       # Same as ground color
    'YELLOW': (255, 215, 0),     # Gold color for seed dots
    'FLOWER': (255, 0, 0)        # Red color for flower dots
} 