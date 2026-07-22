"""
Style Manager Module

This module provides CSS styling for the generated HTML documents.
Includes support for light and dark themes with professional, readable
typography and responsive design.

Features:
    - Light and dark color themes
    - GitHub-flavored Markdown styling
    - Code block syntax highlighting foundation
    - Responsive typography
    - Table of contents styling
    - Print-friendly styles

Author: Carlos Crespo
"""

from enum import Enum


class Theme(Enum):
    """Available color themes for generated HTML."""

    LIGHT = "light"
    DARK = "dark"


class StyleManager:
    """
    Manages CSS styles for HTML document generation.

    Provides comprehensive styling including typography, colors,
    code blocks, lists, blockquotes, and table of contents.

    Attributes:
        theme: The current color theme (LIGHT or DARK).

    Example:
        >>> manager = StyleManager(Theme.DARK)
        >>> css = manager.get_styles()
    """

    # Color palettes for themes
    COLORS = {
        Theme.LIGHT: {
            "bg_primary": "#ffffff",
            "bg_secondary": "#f6f8fa",
            "bg_tertiary": "#f1f3f5",
            "text_primary": "#1f2328",
            "text_secondary": "#656d76",
            "text_muted": "#8b949e",
            "border": "#d0d7de",
            "border_light": "#e8e8e8",
            "link": "#0969da",
            "link_hover": "#0550ae",
            "code_bg": "#f6f8fa",
            "code_text": "#1f2328",
            "blockquote_border": "#d0d7de",
            "blockquote_text": "#656d76",
            "hr": "#d8dee4",
            "toc_bg": "#f6f8fa",
            "toc_border": "#d0d7de",
        },
        Theme.DARK: {
            "bg_primary": "#0d1117",
            "bg_secondary": "#161b22",
            "bg_tertiary": "#21262d",
            "text_primary": "#e6edf3",
            "text_secondary": "#8b949e",
            "text_muted": "#6e7681",
            "border": "#30363d",
            "border_light": "#21262d",
            "link": "#58a6ff",
            "link_hover": "#79c0ff",
            "code_bg": "#161b22",
            "code_text": "#e6edf3",
            "blockquote_border": "#3b434b",
            "blockquote_text": "#8b949e",
            "hr": "#30363d",
            "toc_bg": "#161b22",
            "toc_border": "#30363d",
        },
    }

    def __init__(self, theme: Theme = Theme.LIGHT):
        """
        Initialize the style manager with a theme.

        Args:
            theme: The color theme to use (default: LIGHT).
        """
        self.theme = theme
        self._colors = self.COLORS[theme]

    def get_styles(self) -> str:
        """
        Generate complete CSS stylesheet.

        Returns:
            CSS string with all styles for the HTML document.
        """
        return f"""
/* ========================================
   md2html Generated Styles
   Theme: {self.theme.value}
   Author: Carlos Crespo
   ======================================== */

/* CSS Custom Properties (Variables) */
:root {{
    --color-bg-primary: {self._colors['bg_primary']};
    --color-bg-secondary: {self._colors['bg_secondary']};
    --color-bg-tertiary: {self._colors['bg_tertiary']};
    --color-text-primary: {self._colors['text_primary']};
    --color-text-secondary: {self._colors['text_secondary']};
    --color-text-muted: {self._colors['text_muted']};
    --color-border: {self._colors['border']};
    --color-border-light: {self._colors['border_light']};
    --color-link: {self._colors['link']};
    --color-link-hover: {self._colors['link_hover']};
    --color-code-bg: {self._colors['code_bg']};
    --color-code-text: {self._colors['code_text']};
    --color-blockquote-border: {self._colors['blockquote_border']};
    --color-blockquote-text: {self._colors['blockquote_text']};
    --color-hr: {self._colors['hr']};
    --color-toc-bg: {self._colors['toc_bg']};
    --color-toc-border: {self._colors['toc_border']};

    /* Typography */
    --font-family-base: -apple-system, BlinkMacSystemFont, "Segoe UI",
                        "Noto Sans", Helvetica, Arial, sans-serif,
                        "Apple Color Emoji", "Segoe UI Emoji";
    --font-family-mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas,
                        "Liberation Mono", monospace;
    --font-size-base: 16px;
    --line-height-base: 1.6;

    /* Spacing */
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;

    /* Layout */
    --max-width: 800px;
    --border-radius: 6px;
}}

/* Reset & Base Styles */
*, *::before, *::after {{
    box-sizing: border-box;
}}

html {{
    font-size: var(--font-size-base);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}}

body {{
    margin: 0;
    padding: var(--spacing-xl);
    font-family: var(--font-family-base);
    font-size: 1rem;
    line-height: var(--line-height-base);
    color: var(--color-text-primary);
    background-color: var(--color-bg-primary);
}}

/* Main Container */
.markdown-body {{
    max-width: var(--max-width);
    margin: 0 auto;
    word-wrap: break-word;
}}

/* Content Area */
.content {{
    margin-top: var(--spacing-lg);
}}

/* ========== Typography ========== */

/* Headings */
h1, h2, h3, h4, h5, h6 {{
    margin-top: var(--spacing-xl);
    margin-bottom: var(--spacing-md);
    font-weight: 600;
    line-height: 1.25;
    color: var(--color-text-primary);
}}

h1 {{
    font-size: 2em;
    padding-bottom: 0.3em;
    border-bottom: 1px solid var(--color-border);
}}

h2 {{
    font-size: 1.5em;
    padding-bottom: 0.3em;
    border-bottom: 1px solid var(--color-border);
}}

h3 {{
    font-size: 1.25em;
}}

h4 {{
    font-size: 1em;
}}

h5 {{
    font-size: 0.875em;
}}

h6 {{
    font-size: 0.85em;
    color: var(--color-text-secondary);
}}

/* First heading - no top margin */
.content > h1:first-child,
.content > h2:first-child,
.content > h3:first-child {{
    margin-top: 0;
}}

/* Paragraphs */
p {{
    margin-top: 0;
    margin-bottom: var(--spacing-md);
}}

/* Links */
a {{
    color: var(--color-link);
    text-decoration: none;
    transition: color 0.2s ease;
}}

a:hover {{
    color: var(--color-link-hover);
    text-decoration: underline;
}}

/* Strong & Emphasis */
strong, b {{
    font-weight: 600;
}}

em, i {{
    font-style: italic;
}}

/* ========== Code ========== */

/* Inline Code */
code {{
    padding: 0.2em 0.4em;
    margin: 0;
    font-size: 85%;
    font-family: var(--font-family-mono);
    background-color: var(--color-code-bg);
    color: var(--color-code-text);
    border-radius: var(--border-radius);
    white-space: break-spaces;
}}

/* Code Blocks */
pre {{
    margin-top: 0;
    margin-bottom: var(--spacing-md);
    padding: var(--spacing-md);
    overflow: auto;
    font-size: 85%;
    line-height: 1.45;
    background-color: var(--color-bg-secondary);
    border-radius: var(--border-radius);
    border: 1px solid var(--color-border);
}}

pre code {{
    display: block;
    padding: 0;
    margin: 0;
    overflow: visible;
    line-height: inherit;
    word-wrap: normal;
    background-color: transparent;
    border: 0;
    font-size: 100%;
    white-space: pre;
}}

/* ========== Lists ========== */

ul, ol {{
    margin-top: 0;
    margin-bottom: var(--spacing-md);
    padding-left: 2em;
}}

ul ul, ul ol, ol ul, ol ol {{
    margin-top: var(--spacing-xs);
    margin-bottom: 0;
}}

li {{
    margin-bottom: var(--spacing-xs);
}}

li + li {{
    margin-top: var(--spacing-xs);
}}

/* Unordered lists */
ul {{
    list-style-type: disc;
}}

ul ul {{
    list-style-type: circle;
}}

ul ul ul {{
    list-style-type: square;
}}

/* ========== Blockquotes ========== */

blockquote {{
    margin: 0 0 var(--spacing-md);
    padding: 0 var(--spacing-md);
    color: var(--color-blockquote-text);
    border-left: 0.25em solid var(--color-blockquote-border);
}}

blockquote > :first-child {{
    margin-top: 0;
}}

blockquote > :last-child {{
    margin-bottom: 0;
}}

/* ========== Horizontal Rules ========== */

hr {{
    height: 0.25em;
    margin: var(--spacing-xl) 0;
    padding: 0;
    background-color: var(--color-hr);
    border: 0;
    border-radius: var(--border-radius);
}}

/* ========== Images ========== */

img {{
    max-width: 100%;
    height: auto;
    display: block;
    margin: var(--spacing-md) 0;
    border-radius: var(--border-radius);
}}

/* ========== Table of Contents ========== */

.toc {{
    background-color: var(--color-toc-bg);
    border: 1px solid var(--color-toc-border);
    border-radius: var(--border-radius);
    padding: var(--spacing-md) var(--spacing-lg);
    margin-bottom: var(--spacing-xl);
}}

.toc-title {{
    margin-top: 0;
    margin-bottom: var(--spacing-md);
    font-size: 1.1em;
    font-weight: 600;
    color: var(--color-text-primary);
    border-bottom: none;
    padding-bottom: 0;
}}

.toc-list {{
    margin: 0;
    padding-left: var(--spacing-lg);
    list-style-type: none;
}}

.toc-list ul {{
    margin-top: var(--spacing-xs);
    margin-bottom: 0;
    padding-left: var(--spacing-md);
    list-style-type: none;
}}

.toc-list li {{
    margin-bottom: var(--spacing-xs);
}}

.toc-list a {{
    color: var(--color-text-secondary);
    text-decoration: none;
    transition: color 0.2s ease;
}}

.toc-list a:hover {{
    color: var(--color-link);
    text-decoration: none;
}}

/* ========== Print Styles ========== */

@media print {{
    body {{
        background: white;
        color: black;
        padding: 0;
    }}

    .toc {{
        page-break-after: always;
    }}

    pre {{
        white-space: pre-wrap;
        border: 1px solid #ddd;
    }}

    a {{
        color: black;
        text-decoration: underline;
    }}

    a[href^="http"]::after {{
        content: " (" attr(href) ")";
        font-size: 0.8em;
    }}
}}

/* ========== Responsive Design ========== */

@media (max-width: 768px) {{
    body {{
        padding: var(--spacing-md);
    }}

    h1 {{
        font-size: 1.75em;
    }}

    h2 {{
        font-size: 1.35em;
    }}

    pre {{
        padding: var(--spacing-sm);
        font-size: 80%;
    }}

    .toc {{
        padding: var(--spacing-sm) var(--spacing-md);
    }}
}}

/* ========== Accessibility ========== */

/* Focus styles for keyboard navigation */
a:focus,
button:focus {{
    outline: 2px solid var(--color-link);
    outline-offset: 2px;
}}

/* Reduced motion preference */
@media (prefers-reduced-motion: reduce) {{
    * {{
        transition: none !important;
    }}
}}

/* High contrast mode support */
@media (prefers-contrast: high) {{
    :root {{
        --color-border: currentColor;
        --color-link: blue;
    }}
}}
"""

    def get_minimal_styles(self) -> str:
        """
        Generate minimal CSS for lightweight output.

        Returns:
            Minimal CSS string with only essential styles.
        """
        return f"""
/* Minimal md2html styles */
body {{
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    line-height: 1.6;
    color: {self._colors['text_primary']};
    background: {self._colors['bg_primary']};
}}

pre, code {{
    font-family: monospace;
    background: {self._colors['bg_secondary']};
}}

pre {{
    padding: 1rem;
    overflow: auto;
    border-radius: 6px;
}}

code {{
    padding: 0.2em 0.4em;
    border-radius: 3px;
}}

pre code {{
    padding: 0;
    background: none;
}}

blockquote {{
    margin: 0;
    padding-left: 1rem;
    border-left: 3px solid {self._colors['border']};
    color: {self._colors['text_secondary']};
}}

a {{
    color: {self._colors['link']};
}}

hr {{
    border: none;
    height: 2px;
    background: {self._colors['border']};
}}

.toc {{
    background: {self._colors['bg_secondary']};
    padding: 1rem;
    border-radius: 6px;
    margin-bottom: 2rem;
}}
"""

    def set_theme(self, theme: Theme) -> None:
        """
        Change the current theme.

        Args:
            theme: The new theme to apply.
        """
        self.theme = theme
        self._colors = self.COLORS[theme]

    def get_color(self, color_name: str) -> str:
        """
        Get a specific color value from the current theme.

        Args:
            color_name: Name of the color (e.g., 'bg_primary', 'text_primary').

        Returns:
            The color value as a hex string.

        Raises:
            KeyError: If the color name doesn't exist.
        """
        return self._colors[color_name]
