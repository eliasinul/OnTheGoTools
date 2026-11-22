# Installation Guide

This document covers all methods to install and configure `md2pdf`.

## Quick Start (Recommended)

The fastest way to get started:

```bash
cd OnTheGoTools/md2pdf
./setup.sh
```

This automated script:
1. ✓ Checks for required system tools (pandoc, xelatex, fonts)
2. ✓ Provides installation instructions if anything is missing
3. ✓ Installs the Python package in editable mode
4. ✓ Verifies the installation works

**After running setup.sh:**
```bash
md2pdf --help          # Verify installation
md2pdf examples/example.md  # Try it out
```

## System Dependencies

Before installing the Python package, ensure your system has:

### 1. Pandoc (Document Converter)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install pandoc
```

**macOS:**
```bash
brew install pandoc
```

**Windows:**
- Download from https://pandoc.org/installing.html
- Or use Chocolatey: `choco install pandoc`

**Verify:**
```bash
pandoc --version
```

### 2. TeX Distribution (xelatex + LaTeX packages)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install texlive-xetex texlive-latex-extra texlive-fonts-recommended
```

**macOS:**
```bash
brew install mactex
# Or smaller: brew install mactex-no-gui
```

**Windows:**
- Full TeX Live: https://tug.org/texlive/windows.html
- MiKTeX (simpler): https://miktex.org/download

**Verify:**
```bash
xelatex --version
```

### 3. Fonts (DejaVu Family)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install fonts-dejavu
```

**macOS:**
```bash
brew install font-dejavu
# Or download from https://dejavu-fonts.github.io/
```

**Windows:**
- Download from https://dejavu-fonts.github.io/
- Extract and run installer

**Verify:**
```bash
fc-list | grep DejaVu
```

## Python Installation

Once system dependencies are installed:

### Method 1: Using uv (Recommended for RESource)

```bash
# From repository root
uv pip install -e OnTheGoTools/md2pdf

# Or from the package directory
cd OnTheGoTools/md2pdf
uv pip install -e .
```

### Method 2: Using pip

```bash
# From repository root
pip install -e OnTheGoTools/md2pdf

# Or from the package directory
cd OnTheGoTools/md2pdf
pip install -e .
```

### Method 3: Development Installation (with testing tools)

```bash
uv pip install -e "OnTheGoTools/md2pdf[dev]"
# or
pip install -e "OnTheGoTools/md2pdf[dev]"
```

This also installs pytest, black, and ruff for development.

## Verification

After installation, verify everything works:

```bash
# Check command is available
md2pdf --help

# Try a test conversion
md2pdf OnTheGoTools/md2pdf/examples/example.md -o /tmp/test.pdf

# Check output
ls -lh /tmp/test.pdf
```

If you get a "command not found" error, your Python scripts directory is not on PATH:

```bash
# Try the full Python module invocation
python -m md2pdf.convert --help
```

To add Python scripts to your PATH:

**bash/zsh (~/.bashrc or ~/.zshrc):**
```bash
export PATH="$HOME/.local/bin:$PATH"  # Linux
export PATH="$(python3 -m site --user-scripts):$PATH"  # macOS/Linux alt
```

**Windows (PowerShell):**
```powershell
# Check where pip installs scripts
python -m site --user-scripts
# Add this directory to your PATH via Environment Variables
```

## Installation Locations

### editable (`-e`) mode

Installs with a symlink to the source directory, so changes to source files are reflected immediately:

```bash
uv pip install -e .
```

**Benefits:**
- Changes to Python code are immediately reflected
- Ideal for development
- Remove with: `uv pip uninstall md2pdf`

### Development mode (with `[dev]`)

Installs the package plus development tools:

```bash
uv pip install -e ".[dev]"
```

Includes: pytest, black, ruff for testing and formatting

## Troubleshooting

### "pandoc not found on PATH"

```bash
# Check if pandoc is installed
which pandoc
pandoc --version

# If not installed, see "Pandoc" section above
# If installed but not on PATH, add to ~/.bashrc:
export PATH="/opt/pandoc/bin:$PATH"  # adjust path as needed
```

### "xelatex not found on PATH"

```bash
# Check if xelatex is installed
which xelatex
xelatex --version

# If not installed, see "TeX Distribution" section above
# Common locations:
# Linux: /usr/bin/xelatex
# macOS: /usr/local/bin/xelatex (TeX Live), /Library/TeX/texbin/xelatex (MacTeX)
# Windows: C:\texlive\bin\win32\xelatex.exe or C:\Program Files\MiKTeX\miktex\bin\x64\xelatex.exe
```

### "DejaVu fonts not found"

```bash
# Check installed fonts
fc-list | grep -i dejavu

# If not found, install (see "Fonts" section above)
# macOS: brew install font-dejavu
# Linux: sudo apt install fonts-dejavu
```

### "ModuleNotFoundError: No module named 'md2pdf'"

The package isn't installed correctly. Try:

```bash
# From the md2pdf directory
uv pip install -e .

# Verify installation
python -c "import md2pdf; print(md2pdf.__version__)"
```

### "command not found: md2pdf"

The package is installed but the command isn't on PATH. Use:

```bash
python -m md2pdf.convert document.md
# or find where it was installed
which -a python
python -m site --user-scripts
```

## Uninstalling

```bash
# Using uv
uv pip uninstall md2pdf

# Using pip
pip uninstall md2pdf
```

## Development Setup

For contributors wanting to modify `md2pdf`:

```bash
cd OnTheGoTools/md2pdf

# Install with dev dependencies
uv pip install -e ".[dev]"

# Or use the Makefile
make install-dev

# Run tests
pytest

# Check code style
black --check src/ tests/
ruff check src/ tests/

# Format code
black src/ tests/
ruff check --fix src/ tests/
```

See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for more details.
