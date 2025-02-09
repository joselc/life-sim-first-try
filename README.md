# Life Simulation

[![Tests](https://github.com/joselc/life-sim-first-try/actions/workflows/tests.yml/badge.svg)](https://github.com/joselc/life-sim-first-try/actions/workflows/tests.yml)
[![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)](https://github.com/joselc/life-sim-first-try/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Dependencies](https://img.shields.io/badge/dependencies-pygame-green)](https://www.pygame.org)
[![Repo Size](https://img.shields.io/github/repo-size/joselc/life-sim-first-try)](https://github.com/joselc/life-sim-first-try)
[![codecov](https://codecov.io/gh/joselc/life-sim-first-try/branch/main/graph/badge.svg)](https://codecov.io/gh/joselc/life-sim-first-try)

A Python-based life simulation using a hexagonal grid system. The simulation displays an evolving landscape of plant and ground cells, where plant cells show dynamic growth patterns over time.

## Features

- Hexagonal grid-based world with configurable dimensions
- Dynamic plant lifecycle simulation:
  - Seed stage (yellow dot)
  - Growing stage (expanding green dot)
  - Mature stage (full green)
  - Dying stage (transitioning to brown)
  - Dead stage (brown)
- Natural terrain generation:
  - Ground cells (base terrain)
  - Water bodies (lakes and ponds)
    - Connected groups of 4+ hexagons
    - Up to 30% map coverage
    - Natural, lake-like shapes
- Internationalization support (English and Spanish)
- Configurable simulation speed and grid visibility
- Smooth animations using Pygame
- Pause/Resume functionality
- Help overlay with controls

## Requirements

- Python 3.8+
- Pygame

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd life-sim
```

2. Install dependencies:
```bash
pip install -e .
```

## Usage

Run the simulation:
```bash
python main.py
```

### Controls

- `P`: Pause/Resume simulation
- `H`: Show/Hide help
- `G`: Toggle grid visibility
- `+/-`: Adjust simulation speed
- `L`: Change language
- `ESC`: Return to simulation
- `Q`: Quit

## Configuration

The simulation can be customized by modifying the settings in `src/config.py`:

- Display settings (screen size, FPS)
- Grid dimensions (default: 16x12)
- Plant spawn probability
- Color schemes for different plant states
- Plant lifecycle timings

## Project Structure

```
life-sim/
├── src/
│   ├── hexagons/
│   │   ├── base.py         # Base hexagon class
│   │   ├── plant.py        # Plant cell implementation
│   │   ├── ground.py       # Ground cell implementation
│   │   ├── water.py        # Water cell implementation
│   │   └── plant_states.py # Plant lifecycle management
│   ├── mesh/
│   │   └── hex_mesh.py     # Hexagonal grid implementation
│   ├── renderers/
│   │   ├── base.py         # Base renderer interface
│   │   └── pygame_renderer.py # Pygame implementation
│   ├── i18n/
│   │   ├── strings_en.py   # English strings
│   │   └── strings_es.py   # Spanish strings
│   ├── game_state.py       # Game state management
│   └── config.py           # Configuration settings
├── tests/                  # Test suite
├── main.py                 # Main application entry point
└── run_tests.py           # Test runner
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes (following [Conventional Commits](https://www.conventionalcommits.org/))
4. Push to the branch
5. Create a Pull Request

## Testing

1. Install testing dependencies:
```bash
# Option 1: Install all test dependencies through the package
pip install -e .[test]

# Option 2: Install test dependencies directly
pip install pytest pytest-cov
```

2. Run the tests:
```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=src --cov-report=term-missing

# Run tests and generate HTML coverage report
pytest --cov=src --cov-report=html
```

The HTML coverage report will be generated in the `htmlcov` directory. Open `htmlcov/index.html` in your browser to view it.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 