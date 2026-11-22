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

## Usage

**Setup:**
1. Ensure you have `python` and the required dependencies installed (see [Requirements](#requirements))
2. Navigate to the repository root (or use the full path to `md2pdf`)

**Basic conversion:**
```bash
python OnTheGoTools/md2pdf/convert.py path/to/doc.md
# -> path/to/doc.pdf

python OnTheGoTools/md2pdf/convert.py path/to/doc.md -o output/doc.pdf --no-toc
```

**Options:**
- `-o/--output PATH` — output PDF path (default: input filename with `.pdf` extension)
- `--title TEXT` — override the document title
- `--keep-h1` — don't promote a leading `# Title` line to the title page; keep it as a numbered heading
- `--no-toc` — omit the table of contents
- `--number-sections` — let LaTeX auto-number headings (off by default, since these docs usually number their own `## 1. ...` headings by hand)
- `--highlight-style NAME` — pandoc code highlight theme (default `tango`)
- `--margin SIZE` — page margin, e.g. `1in`, `2.5cm` (default `1in`)
- `--fontsize SIZE` — base font size, e.g. `10pt`, `12pt` (default `11pt`)

**Examples:**
```bash
# Convert notebook.md with custom output location
python OnTheGoTools/md2pdf/convert.py notebooks/my-analysis.md -o results/my-analysis.pdf

# Convert without table of contents and with smaller margins
python OnTheGoTools/md2pdf/convert.py research/notes.md --no-toc --margin 0.75in

# Override title and auto-number sections
python OnTheGoTools/md2pdf/convert.py doc.md --title "Research Report" --number-sections
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

- `pandoc` on `PATH`
- A TeX distribution providing `xelatex`, with `fontspec`, `unicode-math`,
  `fancyhdr`, `booktabs`, `longtable`, `tcolorbox`, `seqsplit`, `etoolbox`,
  `newunicodechar` available (all present in a standard TeX Live install)
- `DejaVu Serif`/`DejaVu Sans`/`DejaVu Sans Mono` fonts installed (used as
  the document fonts; override by editing the `-V mainfont=...` etc. lines
  in `convert.py` if you'd rather use something else)

## Files

- `convert.py` — CLI / importable `convert()` function
- `preamble.tex` — LaTeX injected via `--include-in-header` for the actual styling
