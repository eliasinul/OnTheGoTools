# Architecture

## Overview

`md2pdf` is a lightweight wrapper around Pandoc and XeLaTeX that converts Markdown research notes to beautifully formatted PDFs with consistent styling.

## Core Components

### convert.py

**Entry points:**
- `main(argv)` — CLI entry point for command-line usage
- `cli()` — Installed console script entry point (called by `md2pdf` command)
- `convert(input_path, ...)` — Programmatic API for direct use

**Key functions:**
- `extract_leading_h1(text)` — Extract document title from leading `# Heading`
- `brace_bare_over_under(text)` — Fix TeX compatibility: `\underline x` → `\underline{x}`
- `brace_subscript_macro(text)` — Fix TeX compatibility: `_\mathcal{T}` → `_{\mathcal{T}}`
- `build_pandoc_command(...)` — Construct pandoc invocation with appropriate flags

**Workflow:**
1. Parse CLI arguments or accept function parameters
2. Load Markdown file
3. Apply text preprocessing (extract title, fix TeX)
4. Build pandoc command with XeLaTeX engine
5. Execute pandoc with styled preamble
6. Return output path

### assets/preamble.tex

LaTeX preamble included via `--include-in-header` to inject print-ready styling:
- Page layout (geometry, margins, headers/footers)
- Font configuration (DejaVu for Unicode fallback)
- Table styling (booktabs, alternating rows)
- Code block styling (syntax highlighting, wrapping)
- Math display (unicode-math)
- Color scheme (links, backgrounds)

### tests/

Unit tests covering:
- Title extraction logic
- TeX macro bracing (subscripts, underlines)
- Options parsing
- End-to-end conversion (mocked pandoc)

## Design Principles

1. **No dependencies** — Only wraps existing tools; zero Python package dependencies
2. **Composable** — Separate conversion logic from CLI; importable `convert()` function
3. **Opinionated defaults** — Sensible print-ready styling without tweaking
4. **Override-friendly** — All styling choices are CLI flags
5. **Minimal preprocessing** — Only fix known TeX incompatibilities; don't rewrite user content

## Usage Patterns

### Command Line

```bash
md2pdf document.md -o output.pdf --no-toc --margin 0.75in
```

### Programmatic

```python
from md2pdf.convert import convert
from pathlib import Path

output = convert(
    Path("document.md"),
    title="My Report",
    toc=False,
    margin="0.75in"
)
print(f"Created {output}")
```

### As a Script

```bash
python -m md2pdf.convert document.md
```

## Dependencies

**Runtime:**
- pandoc (external process)
- xelatex (TeX engine, external process)
- Python 3.9+

**Development:**
- pytest (testing)
- black (formatting)
- ruff (linting)

**System:**
- DejaVu fonts (for consistent rendering)

No internal Python dependencies.

## Performance Considerations

- **I/O bound** — Conversion speed is limited by pandoc and xelatex
- **Lazy processing** — Text preprocessing only runs before pandoc
- **No caching** — Each invocation is independent

## Extending

### Adding New Options

1. Add parameter to `convert()` function
2. Add CLI argument to argparse
3. Pass to `build_pandoc_command()`
4. Document in README.md

### Custom LaTeX

Override fonts/styling by editing `assets/preamble.tex` or use `--highlight-style` / `--margin` / `--fontsize` flags.

### Alternative Backends

The architecture is specific to Pandoc + XeLaTeX. Switching to a different PDF engine (e.g., weasyprint) would require:
1. Abstracting conversion logic in `convert.py`
2. Adding engine-specific preprocessing
3. Updating documentation

## Testing Strategy

- **Unit tests** cover text preprocessing (TeX fixes, title extraction)
- **Integration tests** could mock pandoc and validate command construction
- **End-to-end tests** require pandoc + xelatex installed

No tests require internet, external credentials, or large data files.
