.PHONY: help install install-dev setup test lint format clean

help:
	@echo "md2pdf development tasks"
	@echo ""
	@echo "  make setup          - Run automated setup (checks deps, installs package)"
	@echo "  make install        - Install in editable mode"
	@echo "  make install-dev    - Install with dev dependencies"
	@echo "  make test           - Run tests"
	@echo "  make lint           - Check code style"
	@echo "  make format         - Format code with black"
	@echo "  make clean          - Clean build artifacts and cache"
	@echo ""

setup:
	./setup.sh

install:
	uv pip install -e .

install-dev:
	uv pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check src/ tests/
	black --check src/ tests/

format:
	black src/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf build/ dist/ *.egg-info .pytest_cache .ruff_cache
