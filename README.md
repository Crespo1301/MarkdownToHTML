# Markdown to HTML Converter

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-73%20passed-brightgreen.svg)](#testing)

A lightweight, zero-dependency Python tool for converting Markdown files to beautifully styled HTML with automatic table of contents generation.

## Role In The Business

- This repo is one of the public web apps listed in `Portfolio/src/data/projects.ts`.
- It shows CSolutions can ship real tools, not only marketing sites.
- It is both a showcase app and a reusable developer utility.

## Shared Docs

- `AGENTS.md`
- `CLAUDE.md`
- `AI-WORKFLOW.md`
- `SECURITY-CHECKLIST.md`

## Workspace Notes

- Keep README behavior claims aligned with the actual CLI and web flows.
- Treat this repo as a real product surface, not just a code sample.
- When changing parsing behavior, update tests and examples together.

![Light Theme Demo]()

## Features

- **Complete Markdown Support**: Headers, bold, italic, links, images, lists, code blocks, blockquotes, and more
- **Automatic Table of Contents**: Generated from document headers with anchor links
- **Beautiful Themes**: Light and dark themes with GitHub-flavored styling
- **CLI Tool**: Easy command-line interface for single and batch conversions
- **Python API**: Use as a library in your own projects
- **Zero Dependencies**: Pure Python implementation (only pytest for testing)
- **Responsive Design**: Mobile-friendly output with print styles

## Installation

### From Source (Recommended)

```bash
# Clone the repository
git clone https://github.com/Crespo1301/MarkdownToHTML.git
cd MarkdownToHTML

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

### Run Without Installing

If you prefer not to install, you can run directly:

```bash
git clone https://github.com/Crespo1301/MarkdownToHTML.git
cd MarkdownToHTML

# Run with PYTHONPATH
PYTHONPATH=src python -m md2html.cli your_file.md
```

## Quick Start

### Command Line

```bash
# Basic conversion
md2html README.md

# Specify output file
md2html README.md -o docs/readme.html

# Use dark theme
md2html README.md --theme dark

# Disable table of contents
md2html README.md --no-toc

# Batch convert all markdown files
md2html docs/*.md -d output/
```

### Python API

```python
from md2html import MarkdownParser, HTMLConverter
from md2html.styles import Theme

# Parse markdown
parser = MarkdownParser()
tokens = parser.parse("# Hello World\n\nThis is **bold** text.")

# Convert to HTML
converter = HTMLConverter(theme=Theme.LIGHT, include_toc=True)
html = converter.convert(tokens, title="My Document")

# Or use the convenience function
from md2html.converter import convert_markdown_to_html

html = convert_markdown_to_html(
    "# Title\n\nContent here.",
    title="My Doc",
    theme=Theme.DARK,
    include_toc=True
)
```

## Supported Markdown Syntax

### Headers

```markdown
# H1 Header
## H2 Header
### H3 Header
#### H4 Header
##### H5 Header
###### H6 Header
```

### Text Formatting

```markdown
**bold text** or __bold text__
*italic text* or _italic text_
***bold and italic*** or ___bold and italic___
`inline code`
```

### Links and Images

```markdown
[Link Text](https://example.com)
[Link with Title](https://example.com "Title")

![Alt Text](image.png)
![Image with Title](image.png "Title")
```

### Lists

```markdown
Unordered:
- Item 1
- Item 2
  - Nested item
- Item 3

Ordered:
1. First
2. Second
3. Third
```

### Code Blocks

````markdown
```python
def hello():
    print("Hello, World!")
```

    # Or indent with 4 spaces
    code here
````

### Blockquotes

```markdown
> This is a blockquote
> It can span multiple lines
```

### Horizontal Rules

```markdown
---
***
___
```

## CLI Reference

```
usage: md2html [-h] [-o OUTPUT] [-d OUTPUT_DIR] [-t {light,dark}]
               [--no-styles] [--minimal-styles] [--no-toc]
               [--toc-title TOC_TITLE] [--title TITLE] [--fragment]
               [-v] [-q] [--dry-run]
               input [input ...]

Convert Markdown files to beautifully styled HTML

positional arguments:
  input                 Input Markdown file(s) to convert

options:
  -h, --help            show this help message and exit
  --fragment            Output HTML fragment without document wrapper
  -v, --version         show program's version number and exit
  -q, --quiet           Suppress output messages
  --dry-run             Show what would be done without creating files

Output Options:
  -o, --output          Output file path
  -d, --output-dir      Output directory for batch conversions

Styling Options:
  -t, --theme           Color theme: light (default) or dark
  --no-styles           Exclude CSS styles from output
  --minimal-styles      Use minimal CSS instead of full styles

Content Options:
  --no-toc              Disable table of contents generation
  --toc-title           Custom title for table of contents
  --title               Document title (default: from first h1)
```

## Examples

### Basic Conversion

```bash
md2html article.md
# Creates: article.html
```

### Dark Theme with Custom Title

```bash
md2html notes.md -o notes.html --theme dark --title "My Notes"
```

### Batch Processing

```bash
# Convert all markdown files in docs/ to html/
md2html docs/*.md -d html/
```

### HTML Fragment (for embedding)

```bash
md2html content.md --fragment -o partial.html
```

## Project Structure

```
markdown-to-html/
├── src/
│   └── md2html/
│       ├── __init__.py      # Package initialization
│       ├── parser.py        # Markdown parsing engine
│       ├── converter.py     # HTML generation
│       ├── styles.py        # CSS themes and styling
│       └── cli.py           # Command-line interface
├── tests/
│   ├── test_parser.py       # Parser unit tests
│   └── test_converter.py    # Converter unit tests
├── examples/
│   ├── demo.md              # Full feature demonstration
│   └── quickstart.md        # Quick start guide
├── output/                  # Generated HTML files
├── pyproject.toml           # Project configuration
└── README.md
```

## Testing

Run the test suite:

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install test dependencies
pip install pytest

# Run all tests
pytest tests/ -v

# Run with coverage report
pip install pytest-cov
pytest tests/ --cov=md2html --cov-report=html
```

Current test coverage: **73 tests passing**

## API Reference

### MarkdownParser

```python
from md2html import MarkdownParser

parser = MarkdownParser()
tokens = parser.parse(markdown_string)
headers = parser.get_headers()  # For TOC generation
```

### HTMLConverter

```python
from md2html import HTMLConverter
from md2html.styles import Theme

converter = HTMLConverter(
    theme=Theme.LIGHT,      # or Theme.DARK
    include_toc=True,       # Generate table of contents
    toc_title="Contents",   # TOC heading
    include_styles=True     # Embed CSS
)

# Full document
html = converter.convert(tokens, title="My Document")

# HTML fragment only
fragment = converter.convert_fragment(tokens)
```

### StyleManager

```python
from md2html import StyleManager
from md2html.styles import Theme

manager = StyleManager(Theme.DARK)
css = manager.get_styles()           # Full CSS
css = manager.get_minimal_styles()   # Lightweight CSS
```

## Themes

### Light Theme
Clean, professional styling with a white background. Ideal for documentation and reading.

### Dark Theme
Eye-friendly dark mode with carefully selected colors. Perfect for developers and night reading.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Carlos Crespo**
- GitHub: [@Crespo1301](https://github.com/Crespo1301)
- Portfolio: [carloscrespo.info](https://carloscrespo.info)

## Acknowledgments

- Inspired by GitHub Flavored Markdown
- Styling influenced by GitHub's markdown rendering
- Built as part of my software engineering portfolio

---

*Made with ❤️ by Carlos Crespo*
