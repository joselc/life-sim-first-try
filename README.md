# Life Simulation

[![Tests](https://github.com/joselc/life-sim-first-try/actions/workflows/tests.yml/badge.svg)](https://github.com/joselc/life-sim-first-try/actions/workflows/tests.yml)
[![Python Versions](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue)](https://github.com/joselc/life-sim-first-try/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Dependencies](https://img.shields.io/badge/dependencies-pygame-green)](https://www.pygame.org)

A Python-based life simulation using a hexagonal grid system. The simulation displays an evolving landscape of plant and ground cells, where plant cells show dynamic growth patterns over time.

## Features

- Hexagonal grid-based world
- Dynamic plant cells that evolve over time
- Configurable grid size and display settings
- Smooth animations using Pygame

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
pip install pygame
```

## Usage

Run the simulation:
```bash
python main.py
```

## Configuration

The simulation can be customized by modifying the settings in `src/config.py`:

- Display settings (screen size, FPS)
- Grid dimensions
- Plant spawn probability
- Color schemes

## Project Structure

```
life-sim/
├── src/
│   ├── hexagons/
│   │   ├── base.py      # Base hexagon class
│   │   ├── plant.py     # Plant cell implementation
│   │   └── ground.py    # Ground cell implementation
│   ├── mesh/
│   │   └── hex_mesh.py  # Hexagonal grid implementation
│   └── config.py        # Configuration settings
└── main.py              # Main application entry point
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 