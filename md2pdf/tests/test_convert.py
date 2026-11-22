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
