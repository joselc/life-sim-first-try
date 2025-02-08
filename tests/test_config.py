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
    'GREEN': (34, 139, 34),    # Forest green for plants
    'BROWN': (139, 69, 19),    # Saddle brown for ground/soil
    'GRID_LINES': (200, 200, 200)  # Light gray for grid lines
} 