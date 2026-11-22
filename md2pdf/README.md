# md2pdf

Convert a Markdown file into a print-ready PDF (pandoc + xelatex), tuned for
the kind of math-heavy, table-heavy research notes used in research and scientific studies.

## Why use this instead of calling Pandoc directly?

`md2pdf` is a small, opinionated wrapper around Pandoc and XeLaTeX, not a new
Markdown-to-PDF engine. You can run Pandoc directly for a one-off conversion;
this tool exists to make the PDFs in this repository consistent and avoid
repeating a long set of options and document-specific fixes every time.

It applies the same print-oriented page layout, fonts, headers and footers,
table and code-block styling, and link colors by default. It also handles
details that otherwise need manual setup or workarounds: a leading `# Title`
becomes a title page, long inline code wraps, and a couple of TeX constructs
that fail with this XeLaTeX setup are braced before compilation. The options
let you override common choices when a document needs different output.

For a basic PDF or a different layout, use Pandoc directly. Use `md2pdf` when
you want a repeatable, print-ready result with the repository's research-note
defaults.

## Installation

### Quick Start (Automated)

The easiest way to set up `md2pdf` is to run the setup script, which will:
1. Check that system dependencies (pandoc, xelatex, fonts) are installed
2. Install `md2pdf` as a command-line tool
3. Verify everything works

```bash
cd OnTheGoTools/md2pdf
chmod +x setup.sh
./setup.sh
```

This creates a sandboxed environment and makes `md2pdf` available as a command.

### Manual Installation

**Step 1: Install system dependencies**

- **pandoc**: Document converter
  - Ubuntu/Debian: `sudo apt install pandoc`
  - macOS: `brew install pandoc`
  - Windows: https://pandoc.org/installing.html

- **xelatex** (via TeX distribution): LaTeX engine with Unicode support
  - Ubuntu/Debian: `sudo apt install texlive-xetex texlive-latex-extra`
  - macOS: `brew install mactex`
  - Windows: https://miktex.org/download

- **DejaVu fonts**: Used for document rendering
  - Ubuntu/Debian: `sudo apt install fonts-dejavu`
  - macOS: https://dejavu-fonts.github.io/
  - Windows: https://dejavu-fonts.github.io/

**Step 2: Install md2pdf package**

From the repository root or the `OnTheGoTools/md2pdf` directory:

```bash
# Using uv (RESource convention)
uv pip install -e OnTheGoTools/md2pdf

# Or using pip directly
pip install -e OnTheGoTools/md2pdf
```

**Step 3: Verify installation**

```bash
md2pdf --help
```

You should see the help text. If you get a "command not found" error, your
Python scripts directory is not on PATH. Use the full path instead:
```bash
python -m md2pdf.convert --help
```

## Usage

### Basic Conversion

Once installed, convert a Markdown file to PDF:

```bash
md2pdf path/to/document.md
# → creates path/to/document.pdf
```

### Advanced Usage

```bash
# Save to a different location
md2pdf path/to/document.md -o output/report.pdf

# Omit table of contents
md2pdf path/to/document.md --no-toc

# Override title and auto-number sections
md2pdf path/to/document.md --title "My Report" --number-sections

# Customize margins and font size
md2pdf path/to/document.md --margin 0.75in --fontsize 10pt

# Keep leading heading as a numbered section (don't promote to title page)
md2pdf path/to/document.md --keep-h1
```

### Options

- `-o/--output PATH` — output PDF path (default: input filename with `.pdf` extension)
- `--title TEXT` — override the document title
- `--keep-h1` — don't promote a leading `# Title` line to the title page; keep it as a numbered heading
- `--no-toc` — omit the table of contents
- `--number-sections` — let LaTeX auto-number headings (off by default, since these docs usually number their own `## 1. ...` headings by hand)
- `--highlight-style NAME` — pandoc code highlight theme (default `tango`)
- `--margin SIZE` — page margin, e.g. `1in`, `2.5cm` (default `1in`)
- `--fontsize SIZE` — base font size, e.g. `10pt`, `12pt` (default `11pt`)

### Examples

```bash
# Convert notebook.md with custom output location
md2pdf notebooks/my-analysis.md -o results/my-analysis.pdf

# Convert without table of contents and with smaller margins
md2pdf research/notes.md --no-toc --margin 0.75in

# Override title and auto-number sections
md2pdf doc.md --title "Research Report" --number-sections
```

### Without Installing (Direct Script Use)

If you prefer not to install globally, you can run the script directly:

```bash
python OnTheGoTools/md2pdf/convert.py path/to/document.md
python OnTheGoTools/md2pdf/convert.py path/to/document.md -o output/report.pdf --no-toc
```



## What it handles

- A leading `# Title` becomes the document title page instead of a numbered `1 Title` section.
- Math (`$...$`, `$$...$$`), tables, blockquotes (shaded callout boxes), and
  inline/fenced code all render with print-friendly styling (see `preamble.tex`).
- Unicode symbols outside Latin Modern's coverage (e.g. ⚠) fall back to DejaVu Sans.
- Long inline code spans (file paths, module names) wrap instead of
  overflowing the margin.
- `\underline X` / `\overline X` (bare, unbraced single-token arguments) and
  `_\mathcal{T}`-style subscripts on a macro call are automatically braced
  before compiling — both are valid TeX but trip up unicode-math under xelatex.

## Planned features

The following capabilities are planned and are not available yet:

- **Journal-specific style profiles:** provide or select a journal's writing
  and formatting style, based on its author guidelines, rather than relying
  only on the current research-note defaults.
- **DOCX and PDF export:** convert the same Markdown source to either Word
  (`.docx`) or PDF using the selected style profile, so manuscripts can be
  prepared for different submission workflows without maintaining separate
  copies.

## Requirements

### System Requirements

All of these are automatically checked by the setup script:

- **pandoc** (document converter)
  - Required on `PATH`
  - Install: Ubuntu/Debian: `apt install pandoc` | macOS: `brew install pandoc` | Windows: https://pandoc.org/installing.html

- **xelatex** (TeX engine with Unicode support)
  - Requires a TeX distribution (all major TeX packages include this)
  - Required packages: `fontspec`, `unicode-math`, `fancyhdr`, `booktabs`, `longtable`, `tcolorbox`, `seqsplit`, `etoolbox`, `newunicodechar` (all included in standard TeX Live)
  - Install: Ubuntu/Debian: `apt install texlive-xetex texlive-latex-extra` | macOS: `brew install mactex` | Windows: https://miktex.org/

- **DejaVu Fonts** (document rendering)
  - `DejaVu Serif`, `DejaVu Sans`, `DejaVu Sans Mono`
  - Install: Ubuntu/Debian: `apt install fonts-dejavu` | macOS/Windows: https://dejavu-fonts.github.io/

### Python Requirements

- Python 3.9+ (no additional packages required; `md2pdf` only wraps existing tools)

## Project Structure

```
md2pdf/
├── src/md2pdf/              # Main package source code
│   ├── __init__.py         # Package metadata and version
│   └── convert.py          # Core conversion logic and CLI
├── assets/                 # Non-code resources
│   └── preamble.tex       # LaTeX template for print-ready styling
├── tests/                  # Test suite
│   ├── __init__.py        # Test package marker
│   └── test_convert.py    # Unit tests for conversion functions
├── docs/                   # Documentation
│   ├── DEVELOPMENT.md     # Development guide and setup
│   ├── ARCHITECTURE.md    # Technical architecture and design
│   └── CHANGELOG.md       # Version history and releases
├── examples/               # Example Markdown files
│   ├── example.md         # Comprehensive example with all features
│   └── README.md          # Guide to running examples
├── pyproject.toml         # Package metadata, dependencies, entry points
├── pytest.ini             # Pytest configuration
├── .ruff.toml            # Linter and formatter configuration
├── Makefile              # Common development tasks (make help)
├── requirements.txt      # Python dev dependencies
├── setup.sh             # Automated setup and dependency checker
├── .gitignore           # Git ignore patterns
└── README.md            # This file
```

### Key Entry Points

- **[src/md2pdf/convert.py](/local-scratch/localhome/mei3/eliasinul/work/RESource/OnTheGoTools/md2pdf/src/md2pdf/convert.py)** — Main conversion module with CLI and `convert()` API
- **[setup.sh](/local-scratch/localhome/mei3/eliasinul/work/RESource/OnTheGoTools/md2pdf/setup.sh)** — Run this to install and verify dependencies
- **[Makefile](/local-scratch/localhome/mei3/eliasinul/work/RESource/OnTheGoTools/md2pdf/Makefile)** — Run `make help` for common tasks

### Documentation Files

- **[README.md](/local-scratch/localhome/mei3/eliasinul/work/RESource/OnTheGoTools/md2pdf/README.md)** — User guide (this file)
- **[docs/DEVELOPMENT.md](/local-scratch/localhome/mei3/eliasinul/work/RESource/OnTheGoTools/md2pdf/docs/DEVELOPMENT.md)** — Developer setup and workflow
- **[docs/ARCHITECTURE.md](/local-scratch/localhome/mei3/eliasinul/work/RESource/OnTheGoTools/md2pdf/docs/ARCHITECTURE.md)** — Technical design and internals
- **[docs/CHANGELOG.md](/local-scratch/localhome/mei3/eliasinul/work/RESource/OnTheGoTools/md2pdf/docs/CHANGELOG.md)** — Version history

### Example Usage

See [examples/](/local-scratch/localhome/mei3/eliasinul/work/RESource/OnTheGoTools/md2pdf/examples/) for sample Markdown files and how to convert them.
