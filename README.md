# Sokoban AI Solver

A comprehensive Sokoban puzzle solver implementing multiple AI algorithms with performance comparison and caching system.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Algorithms](#algorithms)
- [Performance Testing](#performance-testing)
- [Cache System](#cache-system)
- [Level Sets](#level-sets)
- [Development](#development)
- [Makefile Commands](#makefile-commands)
- [Contributing](#contributing)

## Overview

This project implements a Sokoban puzzle solver using three different AI algorithms:
- **Breadth-First Search (BFS)** - Guarantees optimal solutions
- **Hill Climbing** - Fast heuristic-based approach
- **A*** - Optimal pathfinding with admissible heuristics

The solver includes a visual pygame renderer, comprehensive testing framework, and intelligent caching system to avoid redundant computations.

## Features

- **Cross-Platform Support**: Works on Windows, macOS, and Linux
- **Multiple AI Algorithms**: BFS, Hill Climbing, and A* implementations
- **Visual Rendering**: Pygame-based animation of solution paths
- **Performance Testing**: Comprehensive benchmarking across all levels
- **Intelligent Caching**: Automatic move caching to avoid recomputation
- **Level Management**: Support for multiple level sets (miniCosmos, microCosmos)
- **Interactive Interface**: Command-line interface for algorithm and level selection
- **Statistical Analysis**: Detailed performance comparison and cache statistics
- **Virtual Environment Support**: Automated venv setup and management

## Project Structure

```
asm/
├── src/
│   ├── core/
│   │   ├── state.py          # Game state representation
│   │   ├── game.py           # Game logic and rendering
│   │   └── game_objects.py   # Game object classes
│   ├── algorithm/
│   │   └── solver.py         # AI algorithm implementations
│   └── utils/
│       ├── generator.py      # Level generator from JSON
│       └── levels/
│           └── game.json     # Level definitions
├── tests/
│   ├── simulation.py         # Interactive simulation runner
│   ├── test_bfs.py          # BFS performance testing
│   ├── test_hill_climbing.py # Hill Climbing performance testing
│   ├── test_astar.py        # A* performance testing
│   ├── cache_stats.py       # Cache analysis tools
│   └── utils/
│       ├── move_cache.py    # Cache management system
│       └── move_cache.json  # Cached solutions
├── assets/
│   └── images/              # Game sprites
│       ├── wall.png
│       ├── box.png
│       ├── player.png
│       ├── target.png
│       ├── box_on_target.png
│       └── space.png
├── venv/                    # Virtual environment (created by setup)
├── Makefile                 # Cross-platform build automation
└── README.md               # This file
```

## Installation

### Prerequisites

- Python 3.8+ (3.9+ recommended)
- Make (GNU Make or compatible)
- Git

### Quick Setup (Recommended)

The project includes a cross-platform Makefile that works on both Windows and macOS/Linux.

1. **Clone the repository:**
```bash
git clone <repository-url>
cd asm
```

2. **View available commands:**
```bash
make help
```

3. **Automatic setup with virtual environment:**
```bash
make setup
```

This command will:
- Detect your operating system automatically
- Create a Python virtual environment
- Install all required dependencies (pygame, etc.)
- Display activation instructions for your operating system

4. **Activate the virtual environment:**

**On Windows:**
```cmd
venv\Scripts\activate.bat
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

5. **Verify installation:**
```bash
make simulation
```

### Development Setup

For contributors who want to set up a development environment with additional tools:

```bash
make setup-dev
```

This installs additional development tools:
- pytest (testing framework)
- black (code formatter)
- flake8 (linter)
- mypy (type checker)

### Manual Setup (Alternative)

If you prefer manual setup or the automatic setup doesn't work:

1. **Create virtual environment:**
```bash
python -m venv venv
```

2. **Activate virtual environment:**

**Windows:**
```cmd
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install --upgrade pip
pip install pygame
```

### Troubleshooting

**Common Issues:**

1. **Python not found:** Ensure Python 3.8+ is installed and in your PATH
2. **Make not found:** Install Make for your operating system:
   - Windows: Install via Chocolatey (`choco install make`) or use Git Bash
   - macOS: Install Xcode Command Line Tools (`xcode-select --install`)
   - Linux: Usually pre-installed, or install via package manager

3. **pygame installation fails:** Try upgrading pip first:
```bash
pip install --upgrade pip
pip install pygame
```

4. **Import errors:** Ensure virtual environment is activated and PYTHONPATH is set correctly

## Usage

> **Important:** Always activate your virtual environment before running commands!

### Interactive Simulation

Run the interactive simulation to solve and visualize specific levels:

```bash
make simulation
```

This will:
- Load a predefined level (miniCosmos level_01)
- Check cache for existing solutions
- Run Hill Climbing algorithm if no cached solution exists
- Display animated solution using pygame

### Performance Testing

Test individual algorithms across all levels:

```bash
# Test BFS on all levels
make test-bfs

# Test Hill Climbing on all levels
make test-hill-climbing
# or shorthand:
make test-hill

# Test A* on all levels
make test-astar

# Test all algorithms sequentially
make test-all
```

### Cache Management

View cache statistics and performance comparisons:

```bash
make cache-stats
```

Clean temporary files:

```bash
make clean
```

Complete cleanup (including virtual environment):

```bash
make clean-all
```

## Algorithms

### Breadth-First Search (BFS)
- **Approach**: Explores all possible states level by level
- **Optimality**: Guarantees shortest solution path
- **Time Complexity**: O(b^d) where b is branching factor, d is solution depth
- **Best For**: Finding optimal solutions on smaller levels

### Hill Climbing
- **Approach**: Uses heuristic function to guide search toward goal
- **Optimality**: May not find optimal solution
- **Time Complexity**: Generally faster than BFS
- **Best For**: Quick solutions on complex levels

### A* (A-Star)
- **Approach**: Combines actual cost with heuristic estimate
- **Optimality**: Guarantees optimal solution with admissible heuristic
- **Time Complexity**: O(b^d) in worst case, but typically much faster than BFS
- **Best For**: Optimal solutions with better performance than BFS

### Heuristic Functions

The project implements sophisticated heuristic functions:

- **Manhattan Distance**: Sum of distances from each crate to nearest target
- **Deadlock Detection**: Identifies unsolvable states early
- **Player Distance**: Considers player position in state evaluation

## Performance Testing

### Automated Testing Framework

The testing framework automatically:

1. Loads all levels from the specified set
2. Runs each algorithm with timeout protection
3. Records execution time, move count, and success rate
4. Saves results to JSON files for analysis
5. Updates cache with successful solutions

### Sample Output

```
Testing BFS on miniCosmos levels...
Level level_01: SUCCESS - Time: 2.34s, Moves: 70
Level level_02: SUCCESS - Time: 5.67s, Moves: 45
Level level_03: TIMEOUT - Time: 30.00s
...
Results saved to tests/results_bfs.json
```

### Performance Metrics

Each test records:
- **Execution Time**: Wall clock time to find solution
- **Move Count**: Number of moves in solution path
- **Success Rate**: Percentage of levels solved within timeout
- **Memory Usage**: Peak memory consumption during search

## Cache System

### Automatic Caching

The cache system automatically stores successful solutions to avoid recomputation:

```json
{
  "miniCosmos": {
    "level_01": {
      "bfs": [[0,1], [1,2], [2,3]],
      "hill_climbing": [[0,1], [1,2], [2,4]],
      "a*": [[0,1], [1,2], [2,3]]
    }
  }
}
```

### Cache Benefits

- **Performance**: Instant loading of previously solved levels
- **Comparison**: Easy algorithm performance comparison
- **Persistence**: Solutions persist across sessions
- **Analysis**: Statistical analysis of solution quality

### Cache Management

```bash
# View detailed cache statistics
make cache-stats

# Clean cache files (preserves venv)
make clean

# Complete cleanup including cache and venv
make clean-all
```

## Level Sets

### miniCosmos (40 levels)
- Starter level set with varying difficulty
- Good for algorithm comparison and testing
- Levels: level_01 through level_40

### microCosmos (Additional levels)
- Extended level set for comprehensive testing
- More challenging puzzles
- Supports same algorithm framework

### Adding New Levels

To add new level sets:

1. Add level definitions to `src/utils/levels/game.json`
2. Update `Generator` class if needed
3. Run tests to verify compatibility

## Development

### Code Quality Tools

The development environment includes several code quality tools:

```bash
# Format code with black
make format

# Lint code with flake8
make lint

# Type check with mypy
make type-check
```

### Project Architecture

The project follows a modular architecture:

- **Core Layer**: Game state and rendering logic
- **Algorithm Layer**: AI search implementations
- **Utils Layer**: Level loading and caching
- **Tests Layer**: Performance testing and validation

### Adding New Algorithms

To add a new algorithm:

1. Implement the algorithm in `src/algorithm/solver.py`
2. Add corresponding test file in `tests/`
3. Update Makefile with new test target
4. Add documentation to README

## Makefile Commands

The cross-platform Makefile provides the following commands:

### Setup Commands
```bash
make setup           # Create virtual environment and install dependencies
make setup-dev       # Setup development environment with additional tools
make help           # Display all available commands
```

### Execution Commands
```bash
make simulation      # Run interactive simulation
make test-bfs        # Test BFS algorithm on all levels
make test-hill       # Test Hill Climbing algorithm (alias: test-hill-climbing)
make test-astar      # Test A* algorithm
make test-all        # Run all algorithm tests
```

### Utility Commands
```bash
make cache-stats     # Display cache statistics
make clean           # Clean cache and temporary files
make clean-all       # Clean everything including venv
```

### Development Commands
```bash
make format          # Format code with black
make lint            # Lint code with flake8  
make type-check      # Type check with mypy
```

### Platform Detection

The Makefile automatically detects your operating system and adjusts commands accordingly:
- **Windows**: Uses `python`, Windows path separators, `.bat` activation
- **macOS/Linux**: Uses `python3`, Unix path separators, `source` activation

## Contributing

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Set up development environment: `make setup-dev`
4. Activate virtual environment
5. Implement changes with tests
6. Run quality checks: `make format && make lint && make type-check`
7. Run full test suite: `make test-all`
8. Update documentation as needed
9. Submit pull request

### Code Style

- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Add docstrings for public methods
- Keep functions focused and modular
- Use black for code formatting
- Pass flake8 linting checks

### Testing Guidelines

- Add tests for new algorithms
- Verify cache compatibility
- Test rendering with new features
- Run performance benchmarks
- Ensure cross-platform compatibility

### Virtual Environment

Always work within the virtual environment:

1. Activate environment (see installation section)
2. Install development dependencies: `make setup-dev`
3. Run tests to ensure everything works
4. Develop new features
5. Test across platforms if possible

## License

This project is developed for educational purposes as part of the HCMUT AI course.

## Acknowledgments

- HCMUT Computer Science Department
- Pygame community for rendering framework
- Sokoban puzzle creators and community
- Contributors who helped make this project cross-platform

---

### Quick Start Summary

```bash
# Clone and setup
git clone <repository-url>
cd asm
make setup

# Activate virtual environment
# Windows: venv\Scripts\activate.bat
# macOS/Linux: source venv/bin/activate

# Run simulation
make simulation

# Run all tests
make test-all

# View help
make help
```
