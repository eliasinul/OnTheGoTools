#!/usr/bin/env python3
"""Convert a Markdown file to a print-ready PDF via pandoc + xelatex.

Usage:
    python tools/md2pdf/convert.py INPUT.md [-o OUTPUT.pdf] [--no-toc] [--title TITLE]

A leading "# Title" line is promoted to the document title page (not left as
a numbered "1 Title" section) unless --title overrides it or --keep-h1 is
passed. Section numbering is off by default since these research notes
number their own "## 1. ..." headings by hand; pass --number-sections for
docs that don't.

Requires `pandoc` and a TeX distribution providing `xelatex` on PATH.

```mermaid blocks are rendered to vector PDF via headless Chrome + mermaid.js
(downloaded once to ~/.cache/md2pdf; override with $MD2PDF_MERMAID_JS) and
cropped with `pdfcrop`. Set $MD2PDF_CHROME to pick a browser binary.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
PREAMBLE = PACKAGE_DIR.parent.parent / "assets" / "preamble.tex"

LEADING_H1_RE = re.compile(r"\A\s*# (.+?)\s*\n")

# `\underline x` / `\overline x` (bare single-token argument, no braces) is
# valid TeX but breaks under unicode-math's redefinition of those commands.
# Brace the argument explicitly -- visually identical, safe under any engine.
BARE_OVER_UNDER_RE = re.compile(r"\\(underline|overline)\s+([A-Za-z])(?![A-Za-z{])")


def extract_leading_h1(text: str) -> tuple[str | None, str]:
    """If `text` starts with a level-1 heading, pull it out as a title."""
    match = LEADING_H1_RE.match(text)
    if not match:
        return None, text
    return match.group(1), text[match.end():]


def brace_bare_over_under(text: str) -> str:
    return BARE_OVER_UNDER_RE.sub(r"\\\1{\2}", text)


MATH_SPAN_RE = re.compile(r"\$\$.+?\$\$|(?<![\\$])\$(?!\s)[^$\n]+?(?<!\s)\$", re.DOTALL)
UNESCAPED_SPECIAL_RE = re.compile(r"(?<!\\)([%#])")


def escape_math_specials(text: str) -> str:
    """Escape `%` and `#` inside math spans.

    Raw `%` starts a TeX comment (swallowing the closing braces, e.g.
    "File ended while scanning use of \\frac") and `#` is a parameter
    character; `\\%` / `\\#` render the literal characters.
    """
    return MATH_SPAN_RE.sub(lambda m: UNESCAPED_SPECIAL_RE.sub(r"\\\1", m.group(0)), text)


SUB_SUP_MACRO_RE = re.compile(r"([_^])(\\[A-Za-z]+)(?=\{)")


def brace_subscript_macro(text: str) -> str:
    """Wrap `_\\mathcal{T}` -> `_{\\mathcal{T}}`.

    A subscript/superscript immediately followed by a macro call (rather
    than `_{...}`) hands that macro's *expansion* to the subscript, which
    trips up unicode-math's handling of commands like \\mathcal in that
    position. Wrapping the whole macro call in braces is visually
    identical and avoids the crash.
    """
    out = []
    i = 0
    for match in SUB_SUP_MACRO_RE.finditer(text):
        start = match.start()
        brace_open = match.end()
        depth = 0
        j = brace_open
        while j < len(text):
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        if depth != 0:
            continue  # unbalanced; leave untouched
        out.append(text[i:start])
        out.append(match.group(1) + "{" + match.group(2) + text[brace_open:j + 1] + "}")
        i = j + 1
    out.append(text[i:])
    return "".join(out)


# --- Mermaid ---------------------------------------------------------------
# Pandoc has no Mermaid support, and mermaid-cli (mmdc) needs a modern Node.
# Instead each ```mermaid block is rendered by mermaid.js inside headless
# Chrome, printed to a vector PDF, cropped with pdfcrop, and swapped for an
# image reference before pandoc runs.

MERMAID_VERSION = "11.4.1"
MERMAID_URL = f"https://cdn.jsdelivr.net/npm/mermaid@{MERMAID_VERSION}/dist/mermaid.min.js"
MERMAID_BLOCK_RE = re.compile(
    r"^(?P<fence>`{3,}|~{3,})[ \t]*(?:mermaid|\{[ \t]*\.mermaid(?P<attrs>[^}\n]*)\})[ \t]*\n"
    r"(?P<code>.*?)\n(?P=fence)[ \t]*$",
    re.DOTALL | re.MULTILINE,
)
# Default size on the page: full text width, but never taller than this share
# of the text height (tall TD charts shrink to fit instead of overflowing).
# Override per block: ```{.mermaid width=60%}  or  ```{.mermaid width=9cm height=0.4}
MERMAID_DEFAULT_WIDTH = r"\linewidth"
MERMAID_DEFAULT_MAX_HEIGHT = 0.6
MERMAID_ATTR_RE = re.compile(r"(width|height)\s*=\s*\"?([^\s\"]+)\"?")
CHROME_CANDIDATES = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome")

MERMAID_HTML = """<!doctype html>
<html><head><meta charset="utf-8">
<style>
  @page {{ size: 4000px 4000px; margin: 0; }}
  html, body {{ margin: 0; padding: 0; background: #ffffff; }}
  body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; padding: 8px; }}
  pre.mermaid {{ margin: 0; display: inline-block; }}
</style>
<script src="{js}"></script>
</head><body>
<pre class="mermaid">{code}</pre>
<script>
  mermaid.initialize({{ startOnLoad: false, theme: "neutral", securityLevel: "loose",
                        flowchart: {{ htmlLabels: true }} }});
  mermaid.run().then(() => {{ document.title = "done"; }})
               .catch(e => {{ document.body.innerHTML = "<pre>MERMAID ERROR: " + e + "</pre>"; }});
</script>
</body></html>
"""


def find_chrome() -> str | None:
    override = os.environ.get("MD2PDF_CHROME")
    if override:
        return override
    for name in CHROME_CANDIDATES:
        path = shutil.which(name)
        if path:
            return path
    return None


def mermaid_js_path() -> Path:
    """Local mermaid.min.js: $MD2PDF_MERMAID_JS, else a cached download."""
    override = os.environ.get("MD2PDF_MERMAID_JS")
    if override:
        return Path(override)
    cache = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "md2pdf"
    path = cache / f"mermaid-{MERMAID_VERSION}.min.js"
    if not path.is_file():
        cache.mkdir(parents=True, exist_ok=True)
        print(f"md2pdf: downloading mermaid {MERMAID_VERSION} (one-time) ...", file=sys.stderr)
        with urllib.request.urlopen(MERMAID_URL, timeout=60) as resp:
            data = resp.read()
        tmp = path.with_suffix(".part")
        tmp.write_bytes(data)
        tmp.replace(path)
    return path


def render_mermaid(code: str, out_pdf: Path, *, chrome: str, js: Path) -> Path:
    """Render one Mermaid diagram to a tightly cropped vector PDF."""
    page = out_pdf.with_suffix(".html")
    page.write_text(MERMAID_HTML.format(js=js.as_uri(), code=html.escape(code)), encoding="utf-8")
    raw = out_pdf.with_name(out_pdf.stem + "_page.pdf")
    subprocess.run(
        [chrome, "--headless", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
         "--allow-file-access-from-files", "--virtual-time-budget=20000",
         f"--print-to-pdf={raw}", page.as_uri()],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120,
    )
    if not raw.is_file():
        raise RuntimeError(f"Chrome did not write {raw}")
    subprocess.run(["pdfcrop", "--margins", "2", str(raw), str(out_pdf)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out_pdf


def _latex_length(value: str, unit: str) -> str:
    """'60%' -> 0.6<unit>, '0.4' -> 0.4<unit>, '9cm' / '\\linewidth' -> as given."""
    if value.endswith("%"):
        return f"{float(value[:-1]) / 100:g}{unit}"
    try:
        return f"{float(value):g}{unit}"
    except ValueError:
        return value


def mermaid_latex(pdf: Path, attrs: str = "") -> str:
    """Raw LaTeX that places a rendered diagram, scaled up or down to fit."""
    opts = dict(MERMAID_ATTR_RE.findall(attrs))
    width = _latex_length(opts.get("width", MERMAID_DEFAULT_WIDTH), r"\linewidth")
    height = _latex_length(opts.get("height", str(MERMAID_DEFAULT_MAX_HEIGHT)), r"\textheight")
    return (
        "\n\\begin{center}\n"
        f"\\includegraphics[width={width},height={height},keepaspectratio]{{{pdf.as_posix()}}}\n"
        "\\end{center}\n"
    )


def replace_mermaid_blocks(text: str, workdir: Path) -> str:
    """Swap every ```mermaid fenced block for a rendered PDF image."""
    blocks = list(MERMAID_BLOCK_RE.finditer(text))
    if not blocks:
        return text
    chrome = find_chrome()
    if chrome is None:
        raise RuntimeError("Mermaid block found but no Chrome/Chromium on PATH (set MD2PDF_CHROME)")
    if shutil.which("pdfcrop") is None:
        raise RuntimeError("Mermaid block found but pdfcrop is not on PATH (ships with TeX Live)")
    js = mermaid_js_path()

    def _sub(match: re.Match, counter=iter(range(1, len(blocks) + 1))) -> str:
        code = match.group("code")
        digest = hashlib.sha1(code.encode("utf-8")).hexdigest()[:10]
        pdf = workdir / f"mermaid_{next(counter):02d}_{digest}.pdf"
        render_mermaid(code, pdf, chrome=chrome, js=js)
        return mermaid_latex(pdf, match.group("attrs") or "")

    return MERMAID_BLOCK_RE.sub(_sub, text)


def build_pandoc_command(
    output_path: Path,
    *,
    title: str | None,
    toc: bool,
    number_sections: bool,
    highlight_style: str,
    margin: str,
    fontsize: str,
) -> list[str]:
    cmd = [
        "pandoc",
        "-f",
        "markdown",
        "-o",
        str(output_path),
        "--pdf-engine=xelatex",
        "--standalone",
        "--highlight-style",
        highlight_style,
        "--include-in-header",
        str(PREAMBLE),
        "-V",
        f"geometry:margin={margin}",
        "-V",
        f"fontsize={fontsize}",
        "-V",
        "mainfont=DejaVu Serif",
        "-V",
        "sansfont=DejaVu Sans",
        "-V",
        "monofont=DejaVu Sans Mono",
        "-V",
        "linkcolor=blue",
        "-V",
        "colorlinks=true",
    ]
    if number_sections:
        cmd.append("--number-sections")
    if toc:
        cmd += ["--toc", "--toc-depth=3"]
    if title:
        cmd += ["-M", f"title={title}"]
    return cmd


def convert(
    input_path: Path,
    output_path: Path | None = None,
    *,
    title: str | None = None,
    keep_h1: bool = False,
    toc: bool = True,
    number_sections: bool = False,
    highlight_style: str = "tango",
    margin: str = "1in",
    fontsize: str = "11pt",
) -> Path:
    if shutil.which("pandoc") is None:
        raise RuntimeError("pandoc not found on PATH")
    if shutil.which("xelatex") is None:
        raise RuntimeError("xelatex not found on PATH (install a TeX distribution)")

    input_path = input_path.resolve()
    if not input_path.is_file():
        raise FileNotFoundError(input_path)

    output_path = (output_path or input_path.with_suffix(".pdf")).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    text = input_path.read_text(encoding="utf-8")
    resolved_title = title
    body = text
    if not keep_h1:
        extracted_title, remainder = extract_leading_h1(text)
        if extracted_title:
            body = remainder
            resolved_title = resolved_title or extracted_title
    cmd = build_pandoc_command(
        output_path,
        title=resolved_title,
        toc=toc,
        number_sections=number_sections,
        highlight_style=highlight_style,
        margin=margin,
        fontsize=fontsize,
    )
    with tempfile.TemporaryDirectory(prefix="md2pdf_") as tmp:
        # Mermaid first, so the TeX fix-ups below never touch diagram source.
        body = replace_mermaid_blocks(body, Path(tmp))
        body = brace_bare_over_under(body)
        body = brace_subscript_macro(body)
        body = escape_math_specials(body)
        subprocess.run(cmd, cwd=input_path.parent, input=body, text=True, check=True)
    return output_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Markdown file to convert")
    parser.add_argument("-o", "--output", type=Path, default=None, help="Output PDF path")
    parser.add_argument("--title", default=None, help="Override document title")
    parser.add_argument(
        "--keep-h1",
        action="store_true",
        help="Keep a leading '# Title' line as a numbered section instead of promoting it",
    )
    parser.add_argument("--no-toc", action="store_true", help="Omit table of contents")
    parser.add_argument(
        "--number-sections", action="store_true", help="Let LaTeX auto-number headings"
    )
    parser.add_argument("--highlight-style", default="tango", help="Pandoc code highlight style")
    parser.add_argument("--margin", default="1in", help="Page margin (e.g. 1in, 2.5cm)")
    parser.add_argument("--fontsize", default="11pt", help="Base font size (e.g. 10pt, 11pt, 12pt)")
    args = parser.parse_args(argv)

    try:
        output = convert(
            args.input,
            args.output,
            title=args.title,
            keep_h1=args.keep_h1,
            toc=not args.no_toc,
            number_sections=args.number_sections,
            highlight_style=args.highlight_style,
            margin=args.margin,
            fontsize=args.fontsize,
        )
    except subprocess.CalledProcessError as exc:
        print(f"pandoc failed with exit code {exc.returncode}", file=sys.stderr)
        return exc.returncode
    except (RuntimeError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"wrote {output}")
    return 0


def cli() -> int:
    """Entry point for installed console script."""
    return main()


if __name__ == "__main__":
    raise SystemExit(main())
