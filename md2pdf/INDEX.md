# md2pdf Documentation Index

A comprehensive Python package for converting Markdown to print-ready PDF.

## 🎯 Start Here (Choose Your Path)

### 👤 **For End Users**
1. [QUICK_START.md](QUICK_START.md) ← Installation (2 min)
2. [README.md](README.md) ← Full usage guide
3. [INSTALL.md](INSTALL.md) ← Troubleshooting (if needed)

### 👨‍💻 **For Developers**
1. [STRUCTURE.md](STRUCTURE.md) ← Project organization
2. [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) ← Setup and contributing
3. [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) ← Technical details
4. [src/md2pdf/convert.py](src/md2pdf/convert.py) ← Source code

### 🏢 **For System Administrators**
1. [INSTALL.md](INSTALL.md) ← Detailed system setup
2. [setup.sh](setup.sh) ← Automated installer script
3. [pyproject.toml](pyproject.toml) ← Package configuration

---

## 📚 Complete Documentation Map

### Core Documentation
| Document | Purpose | Audience | Time |
|----------|---------|----------|------|
| [README.md](README.md) | Complete user guide with examples | Everyone | 10 min |
| [QUICK_START.md](QUICK_START.md) | 2-minute installation and usage | New users | 2 min |
| [INSTALL.md](INSTALL.md) | Detailed installation and troubleshooting | Admins | 15 min |

### Developer Documentation  
| Document | Purpose | Audience | Time |
|----------|---------|----------|------|
| [STRUCTURE.md](STRUCTURE.md) | Project layout and organization | Developers | 10 min |
| [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) | Setup, testing, contributing | Contributors | 15 min |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Design, components, extending | Advanced | 15 min |

### Project Information
| Document | Purpose | Audience |
|----------|---------|----------|
| [docs/CHANGELOG.md](docs/CHANGELOG.md) | Version history and releases | Everyone |
| [.FILES_MANIFEST.txt](.FILES_MANIFEST.txt) | Complete file inventory | Admins |
| [INDEX.md](INDEX.md) | This file - documentation map | Everyone |

---

## 🗂️ Directory Guide

### Source Code
- **[src/md2pdf/](src/md2pdf/)** — Python package
  - `__init__.py` — Version and package metadata
  - `convert.py` — Main module with CLI and conversion logic

### Configuration
- **[pyproject.toml](pyproject.toml)** — Package metadata and entry points
- **[pytest.ini](pytest.ini)** — Test configuration
- **[.ruff.toml](.ruff.toml)** — Linter and formatter settings
- **[Makefile](Makefile)** — Development task shortcuts
- **[setup.sh](setup.sh)** — Automated setup script

### Tests
- **[tests/](tests/)** — Test suite
  - `test_convert.py` — Unit tests (10+ test cases)

### Documentation
- **[docs/](docs/)** — Developer documentation
- **[examples/](examples/)** — Sample markdown files and usage guide

### Assets
- **[assets/](assets/)** — Non-code resources
  - `preamble.tex` — LaTeX styling template

---

## 🚀 Quick Commands

### Installation
```bash
./setup.sh                    # Automated setup
# or
uv pip install -e .          # Manual with uv
```

### Usage
```bash
md2pdf document.md           # Convert markdown to PDF
md2pdf --help               # See all options
```

### Development
```bash
make help                     # See all dev tasks
pytest                       # Run tests
make format                  # Format code
make lint                    # Check style
```

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| **Source Code** | ~230 lines (convert.py) |
| **Tests** | ~90 lines, 10+ cases |
| **Documentation** | 10 files, 5000+ lines |
| **Dependencies** | 0 required, 3 optional (dev) |
| **Python Version** | 3.9+ |
| **License** | MIT |
| **Total Files** | 19 tracked files |

---

## 🔍 Search Guide

### Looking for...

**How to install?**
→ [QUICK_START.md](QUICK_START.md) or [INSTALL.md](INSTALL.md)

**How to use the tool?**
→ [README.md](README.md) under "Usage" section

**System dependency issues?**
→ [INSTALL.md](INSTALL.md) "Troubleshooting" section

**How is the project organized?**
→ [STRUCTURE.md](STRUCTURE.md)

**How to contribute?**
→ [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)

**How does it work internally?**
→ [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

**What changed in version X?**
→ [docs/CHANGELOG.md](docs/CHANGELOG.md)

**All the files in this project?**
→ [.FILES_MANIFEST.txt](.FILES_MANIFEST.txt)

**Example usage?**
→ [examples/example.md](examples/example.md) or [examples/README.md](examples/README.md)

---

## 💡 Tips

- **Just getting started?** Read [QUICK_START.md](QUICK_START.md)
- **Want full details?** See [README.md](README.md)
- **Having problems?** Check [INSTALL.md](INSTALL.md)
- **Contributing code?** See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)
- **Need API reference?** Look at [src/md2pdf/convert.py](src/md2pdf/convert.py)
- **Learning the design?** Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 📞 Support Resources

| Issue | Resource |
|-------|----------|
| Installation problems | [INSTALL.md](INSTALL.md) Troubleshooting |
| "pandoc not found" | [INSTALL.md](INSTALL.md) System Dependencies |
| "xelatex not found" | [INSTALL.md](INSTALL.md) TeX Distribution |
| Feature questions | [README.md](README.md) Features section |
| Bug reporting | Provide output from `./setup.sh --system-only` |
| Development setup | [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) |

---

## ✨ What md2pdf Does

Converts Markdown research notes to beautifully formatted print-ready PDFs with:
- ✓ Professional styling and fonts
- ✓ Math support ($...$, $$...$$)
- ✓ Code syntax highlighting
- ✓ Automatic title extraction
- ✓ Customizable layouts
- ✓ No complex dependencies

---

**Last Updated:** 2025-11-22  
**Version:** 0.1.0  
**License:** MIT
