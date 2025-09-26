# Cross-platform Makefile for Sokoban AI Solver
# Supports both Windows and macOS/Linux

# Detect operating system
ifeq ($(OS),Windows_NT)
    DETECTED_OS := Windows
    PYTHON := python
    VENV_BIN := venv\Scripts
    VENV_ACTIVATE := $(VENV_BIN)\activate.bat
    VENV_PYTHON := $(VENV_BIN)\python.exe
    MKDIR := mkdir
    RM := rmdir /s /q
    FIND_CLEAN := for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
    FIND_PYC := del /s /q *.pyc 2>nul || exit 0
else
    DETECTED_OS := $(shell uname -s)
    PYTHON := python3
    VENV_BIN := venv/bin
    VENV_ACTIVATE := $(VENV_BIN)/activate
    VENV_PYTHON := $(VENV_BIN)/python
    MKDIR := mkdir -p
    RM := rm -rf
    FIND_CLEAN := find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    FIND_PYC := find . -name "*.pyc" -delete 2>/dev/null || true
endif

# Default target
.PHONY: help
help:
	@echo "Sokoban AI Solver - Cross-platform Make Commands"
	@echo ""
	@echo "Setup Commands:"
	@echo "  make setup           Create virtual environment and install dependencies"
	@echo "  make setup-dev       Setup development environment with additional tools"
	@echo ""
	@echo "Execution Commands:"
	@echo "  make simulation      Run interactive simulation"
	@echo "  make test-bfs        Test BFS algorithm on all levels"
	@echo "  make test-hill       Test Hill Climbing algorithm"
	@echo "  make test-astar      Test A* algorithm"
	@echo "  make test-all        Run all algorithm tests"
	@echo ""
	@echo "Utility Commands:"
	@echo "  make cache-stats     Display cache statistics"
	@echo "  make clean           Clean cache and temporary files"
	@echo "  make clean-all       Clean everything including venv"
	@echo ""
	@echo "Detected OS: $(DETECTED_OS)"
ifeq ($(DETECTED_OS),Windows)
	@echo "To activate venv: venv\\Scripts\\activate.bat"
else
	@echo "To activate venv: source venv/bin/activate"
endif

# Setup virtual environment
.PHONY: setup
setup:
	@echo "Setting up virtual environment for $(DETECTED_OS)..."
	$(PYTHON) -m venv venv
ifeq ($(DETECTED_OS),Windows)
	@echo "Installing dependencies..."
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install pygame
	@echo ""
	@echo "Setup complete! To activate the virtual environment:"
	@echo "  venv\\Scripts\\activate.bat"
	@echo ""
	@echo "Then run: make simulation"
else
	@echo "Installing dependencies..."
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install pygame
	@echo ""
	@echo "Setup complete! To activate the virtual environment:"
	@echo "  source venv/bin/activate"
	@echo ""
	@echo "Then run: make simulation"
endif

# Setup development environment
.PHONY: setup-dev
setup-dev: setup
	@echo "Installing development dependencies..."
ifeq ($(DETECTED_OS),Windows)
	$(VENV_PYTHON) -m pip install pytest black flake8 mypy
else
	$(VENV_PYTHON) -m pip install pytest black flake8 mypy
endif
	@echo "Development environment setup complete!"

# Check if virtual environment is activated
.PHONY: check-venv
check-venv:
ifndef VIRTUAL_ENV
	@echo "Warning: Virtual environment not activated!"
	@echo "Please run:"
ifeq ($(DETECTED_OS),Windows)
	@echo "  venv\\Scripts\\activate.bat"
else
	@echo "  source venv/bin/activate"
endif
	@echo "Then run your command again."
	@exit 1
endif

# Simulation commands
.PHONY: simulation
simulation:
	@echo "Running Sokoban simulation..."
ifeq ($(DETECTED_OS),Windows)
	@set PYTHONPATH=.;src && set PYTHONWARNINGS=ignore::UserWarning:pygame && $(PYTHON) -m tests.simulation
else
	@PYTHONPATH=.:src PYTHONWARNINGS="ignore::UserWarning:pygame" $(PYTHON) -m tests.simulation
endif
	@$(MAKE) clean

# Algorithm testing commands
.PHONY: test-bfs
test-bfs:
	@echo "Testing BFS algorithm..."
ifeq ($(DETECTED_OS),Windows)
	@set PYTHONPATH=.;src && set PYTHONWARNINGS=ignore::UserWarning && $(PYTHON) -u tests/test_bfs.py
else
	@PYTHONPATH=.:src PYTHONWARNINGS="ignore::UserWarning" $(PYTHON) -u tests/test_bfs.py
endif
	@$(MAKE) clean

.PHONY: test-hill test-hill-climbing
test-hill test-hill-climbing:
	@echo "Testing Hill Climbing algorithm..."
ifeq ($(DETECTED_OS),Windows)
	@set PYTHONPATH=.;src && set PYTHONWARNINGS=ignore::UserWarning && $(PYTHON) -u tests/test_hill_climbing.py
else
	@PYTHONPATH=.:src PYTHONWARNINGS="ignore::UserWarning" $(PYTHON) -u tests/test_hill_climbing.py
endif
	@$(MAKE) clean

.PHONY: test-astar
test-astar:
	@echo "Testing A* algorithm..."
ifeq ($(DETECTED_OS),Windows)
	@set PYTHONPATH=.;src && set PYTHONWARNINGS=ignore::UserWarning && $(PYTHON) -u tests/test_astar.py
else
	@PYTHONPATH=.:src PYTHONWARNINGS="ignore::UserWarning" $(PYTHON) -u tests/test_astar.py
endif
	@$(MAKE) clean

.PHONY: test-all
test-all:
	@echo "Running all algorithm tests..."
	@$(MAKE) test-bfs
	@$(MAKE) test-hill-climbing
	@$(MAKE) test-astar
	@echo "All tests completed!"

# Cache and statistics
.PHONY: cache-stats
cache-stats:
	@echo "Displaying cache statistics..."
ifeq ($(DETECTED_OS),Windows)
	@set PYTHONPATH=.;src && $(PYTHON) tests/cache_stats.py
else
	@PYTHONPATH=.:src $(PYTHON) tests/cache_stats.py
endif

# Cleanup commands
.PHONY: clean
clean:
	@echo "Cleaning temporary files..."
ifeq ($(DETECTED_OS),Windows)
	@$(FIND_PYC)
	@$(FIND_CLEAN)
else
	@$(FIND_PYC)
	@$(FIND_CLEAN)
endif
	@echo "Cleanup complete!"

.PHONY: clean-all
clean-all: clean
	@echo "Removing virtual environment..."
ifeq ($(DETECTED_OS),Windows)
	@if exist venv $(RM) venv
else
	@$(RM) venv
endif
	@echo "Complete cleanup finished!"

# Development commands
.PHONY: format
format:
	@echo "Formatting code with black..."
	$(VENV_PYTHON) -m black src/ tests/

.PHONY: lint
lint:
	@echo "Linting code with flake8..."
	$(VENV_PYTHON) -m flake8 src/ tests/

.PHONY: type-check
type-check:
	@echo "Type checking with mypy..."
	$(VENV_PYTHON) -m mypy src/
