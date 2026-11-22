# md2pdf Quick Start Guide

## 🚀 Installation (< 2 minutes)

```bash
cd OnTheGoTools/md2pdf
./setup.sh
```

This checks system dependencies and installs the tool. Done!

## 📝 Usage

```bash
# Basic conversion
md2pdf document.md

# With options
md2pdf document.md -o output.pdf --no-toc --margin 0.75in

# See all options
md2pdf --help
```

## ✅ Verify Installation

```bash
md2pdf OnTheGoTools/md2pdf/examples/example.md -o /tmp/test.pdf
echo "✓ Installation successful!"
```

## 📚 Documentation

- **[README.md](README.md)** — Full user guide
- **[INSTALL.md](INSTALL.md)** — Installation troubleshooting
- **[docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)** — Contributing guide
- **[STRUCTURE.md](STRUCTURE.md)** — Project organization

## 🛠 Common Tasks

```bash
# Run tests
pytest

# Format code
make format

# Check style
make lint

# See all tasks
make help
```

## 💡 Key Features

✓ Print-ready PDF styling  
✓ Math support ($...$, $$...$$)  
✓ Code syntax highlighting  
✓ Automatic title extraction  
✓ Customizable fonts/margins  
✓ No complex dependencies  

## 🤔 Something Not Working?

1. Check **[INSTALL.md](INSTALL.md)** troubleshooting section
2. Run `./setup.sh --system-only` to verify dependencies
3. Try direct module invocation: `python -m md2pdf.convert --help`

---

**Ready to convert?**
```bash
md2pdf your_document.md
```
