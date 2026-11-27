"""Tests for md2pdf conversion functions."""
import pytest
from pathlib import Path
from md2pdf.convert import (
    extract_leading_h1,
    brace_bare_over_under,
    brace_subscript_macro,
)


class TestExtractLeadingH1:
    """Test leading H1 extraction."""

    def test_extract_title(self):
        """Extract title from leading H1."""
        text = "# My Document\n\nSome content here."
        title, body = extract_leading_h1(text)
        assert title == "My Document"
        assert body == "\nSome content here."

    def test_no_title(self):
        """Return None if no leading H1."""
        text = "Some content without heading."
        title, body = extract_leading_h1(text)
        assert title is None
        assert body == text

    def test_whitespace_handling(self):
        """Handle whitespace around H1."""
        text = "# Title with spaces  \n\nBody text"
        title, body = extract_leading_h1(text)
        assert title == "Title with spaces"
        assert body == "\nBody text"


class TestBraceBareMacros:
    """Test bracing of bare \\underline and \\overline."""

    def test_underline_single_char(self):
        """Brace bare underline."""
        text = r"This is \underline x important."
        result = brace_bare_over_under(text)
        assert result == r"This is \underline{x} important."

    def test_overline_single_char(self):
        """Brace bare overline."""
        text = r"This is \overline y important."
        result = brace_bare_over_under(text)
        assert result == r"This is \overline{y} important."

    def test_already_braced(self):
        """Leave already-braced macros unchanged."""
        text = r"This is \underline{abc} unchanged."
        result = brace_bare_over_under(text)
        assert result == text

    def test_multiple_macros(self):
        """Handle multiple macros in one string."""
        text = r"\underline x and \overline y"
        result = brace_bare_over_under(text)
        assert result == r"\underline{x} and \overline{y}"


class TestBraceSubscriptMacro:
    """Test bracing of subscripts followed by macros."""

    def test_subscript_with_macro(self):
        """Brace subscript macro like _\\mathcal{T}."""
        text = r"Let $_\mathcal{T}$ be the set."
        result = brace_subscript_macro(text)
        assert result == r"Let $_{\\mathcal{T}}$ be the set."

    def test_no_subscript_macro(self):
        """Leave normal subscripts alone."""
        text = r"Let $a_i$ be the index."
        result = brace_subscript_macro(text)
        assert result == text

    def test_superscript_with_macro(self):
        """Handle superscript macros."""
        text = r"Power: $x^\mathbf{n}$ here."
        result = brace_subscript_macro(text)
        assert result == r"Power: $x^{\mathbf{n}}$ here."


class TestMermaidBlocks:
    """Test detection and replacement of ```mermaid fenced blocks."""

    def test_detects_backtick_and_tilde_fences(self):
        from md2pdf.convert import MERMAID_BLOCK_RE

        text = "a\n```mermaid\nflowchart LR\n  A --> B\n```\nb\n~~~{.mermaid}\ngraph TD\n~~~\n"
        codes = [m.group("code") for m in MERMAID_BLOCK_RE.finditer(text)]
        assert codes == ["flowchart LR\n  A --> B", "graph TD"]

    def test_ignores_other_code_blocks(self):
        from md2pdf.convert import MERMAID_BLOCK_RE

        assert not MERMAID_BLOCK_RE.search("```python\nprint(1)\n```\n")

    def test_no_blocks_is_noop(self, tmp_path):
        from md2pdf.convert import replace_mermaid_blocks

        text = "plain text\n```python\nx = 1\n```\n"
        assert replace_mermaid_blocks(text, tmp_path) == text

    def test_block_replaced_by_image(self, tmp_path, monkeypatch):
        import md2pdf.convert as c

        calls = []
        monkeypatch.setattr(c, "find_chrome", lambda: "chrome")
        monkeypatch.setattr(c.shutil, "which", lambda name: "/bin/" + name)
        monkeypatch.setattr(c, "mermaid_js_path", lambda: tmp_path / "m.js")
        monkeypatch.setattr(c, "render_mermaid", lambda code, pdf, **kw: calls.append(code) or pdf)
        out = c.replace_mermaid_blocks("x\n```mermaid\nclassDef a fill:#fff\n```\ny\n", tmp_path)
        assert calls == ["classDef a fill:#fff"]
        assert "```" not in out and "\\includegraphics" in out and ".pdf}" in out

    def test_default_size_fills_width_with_height_cap(self, tmp_path):
        from md2pdf.convert import mermaid_latex

        tex = mermaid_latex(tmp_path / "d.pdf")
        assert r"width=\linewidth,height=0.6\textheight,keepaspectratio" in tex

    def test_size_attributes(self, tmp_path):
        from md2pdf.convert import MERMAID_BLOCK_RE, mermaid_latex

        m = MERMAID_BLOCK_RE.search("```{.mermaid width=60% height=0.3}\ngraph LR\n```\n")
        tex = mermaid_latex(tmp_path / "d.pdf", m.group("attrs"))
        assert r"width=0.6\linewidth,height=0.3\textheight" in tex
        assert r"width=9cm" in mermaid_latex(tmp_path / "d.pdf", "width=9cm")
