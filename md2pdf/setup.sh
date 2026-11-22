#!/bin/bash
# Setup md2pdf for development or use
# 
# Usage:
#   ./setup.sh                  # Install in editable mode (development)
#   ./setup.sh --system-only    # Only check/install system dependencies

set -e

cd "$(dirname "$0")"

SYSTEM_ONLY=false
if [[ "$1" == "--system-only" ]]; then
    SYSTEM_ONLY=true
fi

echo "=== md2pdf Setup ==="
echo ""

# Check system dependencies
echo "Checking system dependencies..."

if ! command -v pandoc &> /dev/null; then
    echo "❌ pandoc not found. Please install it:"
    echo "   - Ubuntu/Debian: sudo apt install pandoc"
    echo "   - macOS: brew install pandoc"
    echo "   - Windows: https://pandoc.org/installing.html"
    exit 1
fi
echo "✓ pandoc found: $(pandoc --version | head -1)"

if ! command -v xelatex &> /dev/null; then
    echo "❌ xelatex not found. Please install a TeX distribution:"
    echo "   - Ubuntu/Debian: sudo apt install texlive-xetex texlive-latex-extra"
    echo "   - macOS: brew install mactex"
    echo "   - Windows: https://miktex.org/download"
    exit 1
fi
echo "✓ xelatex found"

if ! fc-list 2>/dev/null | grep -q "DejaVu"; then
    echo "⚠ DejaVu fonts not found. Installing..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt install fonts-dejavu 2>/dev/null && echo "✓ DejaVu fonts installed" || echo "⚠ Please install fonts-dejavu manually"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "⚠ Install DejaVu fonts from: https://dejavu-fonts.github.io/"
    fi
else
    echo "✓ DejaVu fonts found"
fi

if [[ "$SYSTEM_ONLY" == true ]]; then
    echo ""
    echo "System dependencies check complete!"
    exit 0
fi

echo ""
echo "Installing Python package..."

# Try uv first (RESource convention)
if command -v uv &> /dev/null; then
    echo "Using uv to install in editable mode..."
    uv pip install -e .
elif command -v python3 &> /dev/null; then
    echo "Using pip to install in editable mode..."
    python3 -m pip install -e .
else
    echo "❌ Neither uv nor python3 found on PATH"
    exit 1
fi

echo ""
echo "✓ Setup complete!"
echo ""
echo "You can now use md2pdf:"
echo "  md2pdf path/to/document.md"
echo "  md2pdf path/to/document.md -o output.pdf --no-toc"
echo ""
echo "For more options: md2pdf --help"
