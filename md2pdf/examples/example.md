# Example Research Report

## 1. Introduction

This is an example of a research note that can be converted to PDF using `md2pdf`.
The document demonstrates various formatting options supported by the tool.

### 1.1 Key Features

- **Print-ready styling** with consistent fonts and layout
- **Math support** for equations and symbols
- **Code syntax highlighting** for programming content
- **Tables and figures** rendered professionally
- **Customizable** margins, fonts, and styling

## 2. Mathematical Notation

The tool supports both inline and display math using LaTeX notation:

Inline math: $E = mc^2$ appears in the text naturally.

Display equations are centered:

$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$

Complex subscripts and macros are handled automatically:
- Subscripts: $a_i$ and $b_{i+1}$
- Superscripts: $x^n$ and $y^{2n+1}$

## 3. Code Examples

Inline code like `python --version` and `git commit` are wrapped nicely.

Fenced code blocks with syntax highlighting:

```python
def convert_markdown_to_pdf(input_path, output_path=None):
    """Convert a Markdown file to PDF."""
    output_path = output_path or input_path.with_suffix('.pdf')
    
    text = input_path.read_text(encoding='utf-8')
    # Process and convert to PDF
    return output_path
```

## 4. Tables

| Feature | Supported | Notes |
|---------|-----------|-------|
| Math | Yes | Full LaTeX support |
| Code | Yes | Syntax highlighted |
| Tables | Yes | Professional styling |
| Images | Yes | Pandoc standard |
| Links | Yes | Colored and clickable |

## 5. Blockquotes

> This is a blockquote. It will be rendered with a subtle background and
> distinct styling to set it apart from the main text.
>
> Multiple paragraphs are supported.

## Conclusion

This example demonstrates the capabilities of `md2pdf`. For more information,
see the [README](../README.md) or [Documentation](../docs/DEVELOPMENT.md).
