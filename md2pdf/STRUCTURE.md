# md2pdf Project Structure

## Overview

`md2pdf` is organized with a standard Python package layout for easy distribution and development.

## Directory Layout

```
md2pdf/
├── src/md2pdf/              # Main package source (src layout)
│   ├── __init__.py         # Package metadata (__version__, __author__)
│   └── convert.py          # Core module
│       ├── convert()       # Main conversion function (API)
│       ├── cli()           # Console script entry point
│       ├── main()          # CLI argument parsing
│       └── Helper functions (extract_leading_h1, brace_*, build_pandoc_command)
│
├── assets/                 # Non-code resources
│   └── preamble.tex       # LaTeX template (~2.7 KB)
│       └── Styling for fonts, layout, tables, code blocks, math
│
├── tests/                  # Test suite
│   ├── __init__.py        # Test package marker
│   └── test_convert.py    # Unit tests (~80 lines)
│       ├── TestExtractLeadingH1
│       ├── TestBraceBareMacros
│       └── TestBraceSubscriptMacro
│
├── docs/                   # Developer documentation
│   ├── DEVELOPMENT.md     # Setup, testing, contributing (dev guide)
│   ├── ARCHITECTURE.md    # Design, components, extending
│   └── CHANGELOG.md       # Version history and releases
│
├── examples/               # Example files and documentation
│   ├── example.md         # Comprehensive example (all features)
│   └── README.md          # Guide to running examples
│
├── Configuration and Setup
│   ├── pyproject.toml     # Package metadata, deps, entry points (1 KB)
│   ├── pytest.ini         # Test configuration
│   ├── .ruff.toml        # Linter + formatter settings
│   ├── Makefile          # Development task shortcuts
│   ├── requirements.txt   # Dev dependencies list
│   ├── setup.sh          # Automated dependency installer
│   └── .gitignore        # Git ignore patterns
│
└── Documentation
    ├── README.md         # User guide (this is what most people read)
    ├── INSTALL.md       # Installation troubleshooting
    ├── STRUCTURE.md     # This file
    └── LICENSE          # MIT license
```

## File Purposes

### Core Package (`src/md2pdf/`)

- **__init__.py** (~10 lines)
  - Package version: `__version__ = "0.1.0"`
  - Metadata for imports

- **convert.py** (~220 lines)
  - Conversion logic and text preprocessing
  - Text preprocessing functions:
    - `extract_leading_h1()` → Extract document title
    - `brace_bare_over_under()` → Fix `\underline x` → `\underline{x}`
    - `brace_subscript_macro()` → Fix `_\mathcal{T}` → `_{\mathcal{T}}`
  - Pandoc integration:
    - `build_pandoc_command()` → Construct pandoc flags
  - Main APIs:
    - `convert()` → Programmatic conversion
    - `main()` → CLI parser
    - `cli()` → Entry point for installed command

### Assets (`assets/`)

- **preamble.tex** (~100 lines)
  - LaTeX template injected via `--include-in-header`
  - Defines fonts, spacing, table styling, colors, etc.
  - Loaded by convert.py at runtime

### Tests (`tests/`)

- **test_convert.py** (~90 lines)
  - 10+ unit tests covering core functions
  - Tests title extraction, macro bracing, text preprocessing
  - No external dependencies (self-contained test data)
  - Run: `pytest` or `python -m pytest tests/`

### Documentation

- **README.md** (the main guide)
  - What md2pdf is
  - Installation (3 methods)
  - Usage with examples
  - Requirements
  - Feature list

- **INSTALL.md**
  - Detailed system dependency installation
  - Troubleshooting common issues
  - PATH configuration help

- **docs/DEVELOPMENT.md**
  - Setup for contributors
  - Running tests and linting
  - Project conventions

- **docs/ARCHITECTURE.md**
  - Design decisions
  - Component descriptions
  - Extending the tool

- **docs/CHANGELOG.md**
  - Version history
  - What changed in each release

### Configuration

- **pyproject.toml**
  - Package name, version, description
  - Python version requirement (>=3.9)
  - Dependencies (zero runtime, dev optional)
  - Entry point: `md2pdf = "md2pdf.convert:cli"`
  - Setuptools configuration for src layout

- **pytest.ini**
  - Test discovery patterns
  - Verbosity settings
  - Custom test markers

- **.ruff.toml**
  - Linting rules (pycodestyle, pyflakes, isort, etc.)
  - Code formatting preferences
  - Black line length

- **Makefile**
  - `make setup` → Run setup.sh
  - `make test` → pytest
  - `make lint` → ruff + black check
  - `make format` → auto-format code
  - `make clean` → remove build artifacts

- **setup.sh** (executable)
  - System dependency checker
  - Provides install instructions
  - Installs Python package

## Workflow

### For Users

1. Run `./setup.sh` (automated setup)
2. Use `md2pdf document.md`
3. See README.md for options

### For Developers

1. `uv pip install -e ".[dev]"` (editable + dev tools)
2. Edit `src/md2pdf/convert.py` or `tests/test_convert.py`
3. `pytest` to test
4. `make format` to format
5. `make lint` to check
6. Git commit

### For Contributors

1. Fork repository
2. `./setup.sh` to set up
3. Create feature branch
4. Make changes in `src/md2pdf/`
5. Add tests in `tests/`
6. `pytest` and `make lint`
7. Submit pull request

## Package Distribution

The package can be distributed via:

- **pip/uv** (from local directory)
  ```bash
  uv pip install -e OnTheGoTools/md2pdf
  ```

- **PyPI** (future, requires build + upload)
  ```bash
  python -m build
  python -m twine upload dist/
  ```

## Size and Complexity

- **Total lines of code:** ~230 (convert.py)
- **Total tests:** ~90 lines, 10+ test cases
- **Dependencies:** 0 (zero required, 3 optional for dev)
- **Package size:** ~20 KB (without assets)
- **Installation size:** Minimal (no heavy deps)

## Key Design Principles

1. **Minimal footprint** — Only essential files, no cruft
2. **Clear separation** — Code (src), assets (assets), tests (tests), docs (docs)
3. **Standard layout** — Follows Python community conventions
4. **Easy to modify** — Each component is self-contained
5. **Developer-friendly** — Makefile shortcuts, good documentation
