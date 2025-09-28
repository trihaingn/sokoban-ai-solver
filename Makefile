# Cross-platform Makefile for Sokoban AI Solver
# Supports Windows, macOS, and Linux
.SILENT:

# Platform detection
ifeq ($(OS),Windows_NT)
    PYTHON = python
    VENV_ACTIVATE = venv\Scripts\activate.bat
    VENV_DEACTIVATE = venv\Scripts\deactivate.bat
    VENV_PYTHON = venv\Scripts\python.exe
    RM_RF = rmdir /s /q
    MKDIR = mkdir
    PATH_SEP = \\
	CLEAN_MOVE_CACHE = if exist "tests\utils\move_cache.json" del "tests\utils\move_cache.json"
	CREATE_CACHE_DIR = if not exist "tests\utils" mkdir "tests\utils"
	CREATE_CACHE_FILE = echo {} > "tests\utils\move_cache.json"
    CLEAN_PYCACHE = for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
    CLEAN_PYC = del /s /q *.pyc *.pyo 2>nul || true
	BLUE=
    RESET=
else
    PYTHON = python3
    VENV_ACTIVATE = source venv/bin/activate
    VENV_DEACTIVATE = deactivate
    VENV_PYTHON = venv/bin/python
    RM_RF = rm -rf
    MKDIR = mkdir -p
    PATH_SEP = /
	CLEAN_MOVE_CACHE = rm -f tests/utils/move_cache.json 2>/dev/null || true
	CREATE_CACHE_DIR = mkdir -p tests/utils
	CREATE_CACHE_FILE = echo '{}' > tests/utils/move_cache.json
    CLEAN_PYCACHE = find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    CLEAN_PYC = find . -name "*.pyc" -delete 2>/dev/null || true; find . -name "*.pyo" -delete 2>/dev/null || true
	BLUE=\033[34m
    RESET=\033[0m
endif

.PHONY: help setup simulation test-bfs test-hybrid-heuristic clean clear

# Default target
help:
	@echo "Sokoban AI Solver - Available Commands:"
	@echo ""
	@echo "Setup Commands:"
	@echo "  make setup              - Create virtual environment and install dependencies"
	@echo ""
	@echo "Execution Commands:"
	@echo "  make simulation         - Run interactive simulation"
	@echo "  make test-bfs           - Test BFS algorithm"
	@echo "  make test-hybrid-heuristic - Test Hybrid Heuristic algorithm"
	@echo ""
	@echo "Utility Commands:"
	@echo "  make clean              - Remove Python cache files"
	@echo "  make clear              - Remove virtual environment and cache files"
	@echo "  make help               - Show this help message"
	@echo ""
	@echo "Platform: $(if $(findstring Windows_NT,$(OS)),Windows,Unix-like)"

setup:
	@echo "Setting up virtual environment..."
	$(PYTHON) -m venv venv
	@echo ""
	@echo "Installing requirements..."
ifeq ($(OS),Windows_NT)
	venv\Scripts\pip.exe install -r requirements.txt
	@echo ""
	@echo "Setup complete! To activate the virtual environment, run:"
	@echo "$(BLUE)  venv\Scripts\activate.bat"
	@echo ""
	@echo "To deactivate when done, run:"
	@echo "$(BLUE)  venv\Scripts\deactivate.bat"
else
	venv/bin/pip install -r requirements.txt
	@echo ""
	@echo "Setup complete! To activate the virtual environment, run:"
	@echo "$(BLUE)  source venv/bin/activate$(RESET)"
	@echo ""
	@echo "To deactivate when done, run:"
	@echo "$(BLUE)  deactivate$(RESET)"
endif
	@echo ""

simulation:
	@echo "Running simulation..."
	$(PYTHON) -m tests.simulation.simulation
	$(MAKE) clean

test-bfs:
	@echo "Running BFS tests..."
	$(PYTHON) -m tests.algorithm_tests.test_bfs
	$(MAKE) clean

test-hybrid-heuristic:
	@echo "Running Hybrid Heuristic tests..."
	$(PYTHON) -m tests.algorithm_tests.test_hybrid_heuristic
	$(MAKE) clean

clean:
	@echo "Cleaning Python cache files..."
ifeq ($(OS),Windows_NT)
	@$(CLEAN_PYCACHE)
	@$(CLEAN_PYC)
else
	@$(CLEAN_PYCACHE)
	@$(CLEAN_PYC)
endif
	@echo "Clean complete."

clear:
	@echo "Removing virtual environment and cache files..."
ifeq ($(OS),Windows_NT)
	@$(CLEAN_PYCACHE)
	@$(CLEAN_PYC)
	@if exist venv $(RM_RF) venv
	@echo "Removing moving cache..."
	@$(CLEAN_MOVE_CACHE)
	@$(CREATE_CACHE_DIR)
	@$(CREATE_CACHE_FILE)
else
	@$(CLEAN_PYCACHE)
	@$(CLEAN_PYC)
	@$(RM_RF) venv
	@echo "Removing moving cache..."
	@$(CLEAN_MOVE_CACHE)
	@$(CREATE_CACHE_DIR)
	@$(CREATE_CACHE_FILE)
endif
	@echo "Clear complete."
