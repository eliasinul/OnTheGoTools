# md2pdf Examples

This directory contains example Markdown files that demonstrate the capabilities of `md2pdf`.

## Running Examples

### Basic Conversion

```bash
cd ../
md2pdf examples/example.md -o /tmp/example.pdf
```

### With Custom Options

```bash
# No table of contents, smaller margins
md2pdf examples/example.md -o /tmp/example-compact.pdf --no-toc --margin 0.75in

# Auto-numbered sections, larger font
md2pdf examples/example.md -o /tmp/example-numbered.pdf --number-sections --fontsize 12pt
```

## Example Files

- **example.md** — Comprehensive example covering math, code, tables, and formatting

## Creating Your Own Examples

1. Create a `.md` file in this directory
2. Run `md2pdf your-file.md` from the parent directory
3. Check the output PDF

For more detailed documentation, see:
- [README.md](../README.md) — User guide
- [docs/DEVELOPMENT.md](../docs/DEVELOPMENT.md) — Development guide
- [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) — Technical details
