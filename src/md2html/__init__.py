"""
md2html - A Markdown to HTML Converter

A lightweight, extensible Python tool for converting Markdown files to 
beautifully styled HTML with automatic table of contents generation.

Author: Carlos Crespo
GitHub: https://github.com/Crespo1301/MarkdownToHTML
License: MIT
"""

__version__ = "2.0.0"
__author__ = "Carlos Crespo"

# Public API exports
from .parser import MarkdownParser
from .converter import HTMLConverter
from .styles import StyleManager

__all__ = [
    "MarkdownParser",
    "HTMLConverter", 
    "StyleManager",
    "__version__",
    "__author__",
]
