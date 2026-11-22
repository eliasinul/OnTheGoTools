# Development Guide

## Setup

### Quick Start

```bash
cd OnTheGoTools/md2pdf
./setup.sh
```

### Manual Setup

1. **Install system dependencies:**
   ```bash
   ./setup.sh --system-only
   ```

2. **Install in development mode:**
   ```bash
   # Using uv (RESource convention)
   uv pip install -e .
   
   # Or using pip
   pip install -e .[dev]
   ```

3. **Verify:**
   ```bash
   md2pdf --help
   pytest tests/
   ```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_convert.py

# Run specific test
pytest tests/test_convert.py::TestExtractLeadingH1::test_extract_title
```

## Linting and Formatting

```bash
# Format code
black src/ tests/

# Check code style
ruff check src/ tests/

# Fix style issues
ruff check --fix src/ tests/
```

## Project Structure

```
md2pdf/
├── src/md2pdf/           # Main package
│   ├── __init__.py      # Package metadata
│   └── convert.py       # CLI and conversion logic
├── assets/              # Non-code resources
│   └── preamble.tex    # LaTeX template for styling
├── tests/               # Test suite
│   ├── __init__.py
│   └── test_convert.py
├── docs/                # Documentation
│   └── DEVELOPMENT.md   # This file
├── pyproject.toml       # Package metadata and config
├── requirements.txt     # Python dependencies
├── setup.sh            # Automated setup script
├── README.md           # User guide
└── .gitignore          # Git ignore patterns
```

## Adding Features

1. **Add code** to `src/md2pdf/`
2. **Add tests** to `tests/`
3. **Update docs** in README.md or docs/
4. **Test locally:** `pytest`
5. **Format:** `black src/ tests/`
6. **Commit** with meaningful message

## Releasing

Before creating a release:

1. Update version in `src/md2pdf/__init__.py` and `pyproject.toml`
2. Update README.md with any new features
3. Run full test suite: `pytest`
4. Commit changes: `git commit -m "Release v0.x.x"`
5. Create git tag: `git tag v0.x.x`
6. Push: `git push && git push --tags`

For PyPI distribution:
```bash
# Build distribution
python -m build

# Upload to PyPI (requires credentials)
python -m twine upload dist/
```
