# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-22

### Added
- Initial release of `md2pdf`
- Markdown to PDF conversion via pandoc + xelatex
- Print-ready styling with consistent fonts and layout
- Automatic title page extraction from leading `# Title` heading
- Table of contents generation (can be disabled)
- Code syntax highlighting with customizable themes
- TeX compatibility fixes for unicode-math
- Configurable margins, font sizes, and styling
- Command-line interface with `md2pdf` command
- Programmatic API via `convert()` function
- Comprehensive test suite
- Automated setup script for dependency installation
- Full documentation in README, DEVELOPMENT, and ARCHITECTURE guides

### Technical Details
- Python 3.9+ support
- Zero Python package dependencies
- External dependencies: pandoc, xelatex, DejaVu fonts

## Planned Features

- Journal-specific style profiles
- DOCX export support
- Custom template support
- Bibliography/citation integration
