"""
HTML Converter Module

This module provides the HTMLConverter class that transforms parsed Markdown
tokens into complete, styled HTML documents with optional table of contents.

Features:
    - Full HTML document generation with proper DOCTYPE and meta tags
    - Automatic table of contents generation from headers
    - Customizable CSS styling
    - Syntax highlighting support for code blocks
    - Responsive design output
    - Dark mode support

Author: Carlos Crespo
"""

import html
import re
from typing import List, Optional, Tuple
from .parser import Token, TokenType, MarkdownParser
from .styles import StyleManager, Theme


class HTMLConverter:
    """
    Converts parsed Markdown tokens into complete HTML documents.

    The converter takes tokens from the MarkdownParser and generates
    well-structured HTML with optional styling and table of contents.

    Attributes:
        style_manager: StyleManager instance for CSS generation.
        include_toc: Whether to generate a table of contents.
        toc_title: Title for the table of contents section.

    Example:
        >>> converter = HTMLConverter(include_toc=True)
        >>> html = converter.convert(tokens, title="My Document")
    """

    def __init__(
        self,
        theme: Theme = Theme.LIGHT,
        include_toc: bool = True,
        toc_title: str = "Table of Contents",
        include_styles: bool = True,
    ):
        """
        Initialize the HTML converter.

        Args:
            theme: Color theme for the generated HTML (LIGHT or DARK).
            include_toc: Whether to include a table of contents.
            toc_title: Title text for the TOC section.
            include_styles: Whether to embed CSS styles in the output.
        """
        self.style_manager = StyleManager(theme)
        self.include_toc = include_toc
        self.toc_title = toc_title
        self.include_styles = include_styles
        self._headers: List[Token] = []

    def convert(
        self,
        tokens: List[Token],
        title: str = "Document",
        headers: Optional[List[Token]] = None,
    ) -> str:
        """
        Convert parsed tokens into a complete HTML document.

        Args:
            tokens: List of Token objects from the parser.
            title: HTML document title (appears in browser tab).
            headers: Optional list of header tokens for TOC generation.
                    If not provided, extracts headers from tokens.

        Returns:
            Complete HTML document as a string.
        """
        self._headers = headers or self._extract_headers(tokens)

        # Generate main content
        body_content = self._convert_tokens(tokens)

        # Generate table of contents if enabled
        toc_html = ""
        if self.include_toc and self._headers:
            toc_html = self._generate_toc()

        # Build complete document
        return self._build_document(title, toc_html, body_content)

    def convert_fragment(
        self, tokens: List[Token], headers: Optional[List[Token]] = None
    ) -> str:
        """
        Convert tokens to HTML without a document wrapper.

        Useful for embedding converted Markdown in existing HTML pages or a
        CMS. When ``include_toc`` is enabled and headers are present, the
        table of contents is prepended to the fragment so fragment output
        behaves consistently with ``convert()`` instead of silently
        dropping the setting.

        Args:
            tokens: List of Token objects from the parser.
            headers: Optional list of header tokens for TOC generation.
                    If not provided, extracts headers from tokens.

        Returns:
            HTML fragment string (no DOCTYPE, html, head, body tags).
        """
        self._headers = (
            headers if headers is not None else self._extract_headers(tokens)
        )
        body_content = self._convert_tokens(tokens)

        if self.include_toc and self._headers:
            toc_html = self._generate_toc()
            return f"{toc_html}\n\n{body_content}" if body_content else toc_html

        return body_content

    def _extract_headers(self, tokens: List[Token]) -> List[Token]:
        """
        Extract all header tokens from the token list.

        Args:
            tokens: List of all tokens.

        Returns:
            List containing only header tokens.
        """
        return [t for t in tokens if t.type == TokenType.HEADER]

    def _convert_tokens(self, tokens: List[Token]) -> str:
        """
        Convert a list of tokens to HTML.

        Args:
            tokens: List of Token objects to convert.

        Returns:
            HTML string representation of the tokens.
        """
        html_parts = []

        for token in tokens:
            html = self._convert_token(token)
            if html:
                html_parts.append(html)

        return "\n\n".join(html_parts)

    def _convert_token(self, token: Token) -> str:
        """
        Convert a single token to HTML.

        Args:
            token: The Token to convert.

        Returns:
            HTML string for the token.
        """
        converters = {
            TokenType.HEADER: self._convert_header,
            TokenType.PARAGRAPH: self._convert_paragraph,
            TokenType.CODE_BLOCK: self._convert_code_block,
            TokenType.BLOCKQUOTE: self._convert_blockquote,
            TokenType.UNORDERED_LIST: self._convert_unordered_list,
            TokenType.ORDERED_LIST: self._convert_ordered_list,
            TokenType.HORIZONTAL_RULE: self._convert_horizontal_rule,
        }

        converter = converters.get(token.type)
        if converter:
            return converter(token)

        return ""

    def _convert_header(self, token: Token) -> str:
        """
        Convert a header token to HTML heading element.

        Args:
            token: Header token with level and content.

        Returns:
            HTML heading tag (h1-h6) with id attribute.
        """
        level = token.level
        content = token.content
        header_id = token.id

        return f'<h{level} id="{header_id}">{content}</h{level}>'

    def _convert_paragraph(self, token: Token) -> str:
        """
        Convert a paragraph token to HTML paragraph element.

        Args:
            token: Paragraph token with content.

        Returns:
            HTML paragraph tag.
        """
        return f"<p>{token.content}</p>"

    def _convert_code_block(self, token: Token) -> str:
        """
        Convert a code block token to HTML pre/code elements.

        Args:
            token: Code block token with content and optional language.

        Returns:
            HTML pre and code tags with syntax highlighting class.
        """
        content = self._escape_code_html(token.content)
        language_name = token.language.split(maxsplit=1)[0] if token.language else ""
        language = re.sub(r"[^a-zA-Z0-9_+-]", "", language_name)[:40]

        if language:
            return f'<pre><code class="language-{language}">{content}</code></pre>'
        return f"<pre><code>{content}</code></pre>"

    def _convert_blockquote(self, token: Token) -> str:
        """
        Convert a blockquote token to HTML blockquote element.

        Args:
            token: Blockquote token with content.

        Returns:
            HTML blockquote tag.
        """
        # Handle multi-line blockquotes
        lines = token.content.split("\n")
        formatted_lines = [f"<p>{line}</p>" if line.strip() else "" for line in lines]
        inner_content = "\n".join(filter(None, formatted_lines))

        if not inner_content:
            inner_content = f"<p>{token.content}</p>"

        return f"<blockquote>\n{inner_content}\n</blockquote>"

    def _convert_unordered_list(self, token: Token) -> str:
        """
        Convert an unordered list token to HTML ul/li elements.

        Handles nested lists by tracking indentation levels.

        Args:
            token: Unordered list token with children list items.

        Returns:
            HTML unordered list structure.
        """
        return self._convert_list(token.children, ordered=False)

    def _convert_ordered_list(self, token: Token) -> str:
        """
        Convert an ordered list token to HTML ol/li elements.

        Args:
            token: Ordered list token with children list items.

        Returns:
            HTML ordered list structure.
        """
        return self._convert_list(token.children, ordered=True)

    def _convert_list(self, items: List[Token], ordered: bool = False) -> str:
        """
        Convert list items to HTML list structure.

        Handles nested lists by recursively building nested ul/ol elements.

        Args:
            items: List of LIST_ITEM tokens.
            ordered: True for ordered lists, False for unordered.

        Returns:
            HTML list string.
        """
        if not items:
            return ""

        tag = "ol" if ordered else "ul"
        html_parts = [f"<{tag}>"]

        current_level = 0

        for item in items:
            item_level = item.level

            # Handle nesting
            while current_level < item_level:
                html_parts.append(f"<{tag}>")
                current_level += 1

            while current_level > item_level:
                html_parts.append(f"</{tag}>")
                html_parts.append("</li>")
                current_level -= 1

            html_parts.append(f"<li>{item.content}</li>")

        # Close any remaining nested lists
        while current_level > 0:
            html_parts.append(f"</{tag}>")
            current_level -= 1

        html_parts.append(f"</{tag}>")

        return "\n".join(html_parts)

    def _convert_horizontal_rule(self, token: Token) -> str:
        """
        Convert a horizontal rule token to HTML hr element.

        Args:
            token: Horizontal rule token.

        Returns:
            HTML hr tag.
        """
        return "<hr>"

    def _generate_toc(self) -> str:
        """
        Generate a table of contents from collected headers.

        Builds a tree from the flat header list (based on heading level)
        and renders it as properly nested `<ul><li>` markup, so a nested
        `<ul>` is always a child of the `<li>` it belongs under rather than
        a direct, invalid sibling of another `<ul>`. Handles arbitrary
        level jumps (e.g. an h1 followed directly by an h3) by nesting the
        deeper heading under the closest preceding shallower heading.

        Returns:
            HTML string containing the TOC.
        """
        if not self._headers:
            return ""

        # Each stack entry is (level, children_list_to_append_into).
        root: list = []
        stack: List[Tuple[int, list]] = [(0, root)]

        for header in self._headers:
            while len(stack) > 1 and stack[-1][0] >= header.level:
                stack.pop()
            node_children: list = []
            stack[-1][1].append((header, node_children))
            stack.append((header.level, node_children))

        def render(nodes, list_class: str = "") -> str:
            if not nodes:
                return ""
            class_attr = f' class="{list_class}"' if list_class else ""
            items = []
            for header, children in nodes:
                clean_content = self._strip_html_tags(header.content)
                entry = f'<a href="#{header.id}">{clean_content}</a>'
                nested = render(children)
                if nested:
                    items.append(f"<li>{entry}\n{nested}\n</li>")
                else:
                    items.append(f"<li>{entry}</li>")
            return f"<ul{class_attr}>\n" + "\n".join(items) + "\n</ul>"

        toc_list = render(root, list_class="toc-list")
        return (
            '<nav class="toc">\n'
            f'<h2 class="toc-title">{self.toc_title}</h2>\n'
            f"{toc_list}\n"
            "</nav>"
        )

    def _build_document(self, title: str, toc_html: str, body_content: str) -> str:
        """
        Build a complete HTML document.

        Args:
            title: Document title for the <title> tag.
            toc_html: Generated table of contents HTML.
            body_content: Main document content HTML.

        Returns:
            Complete HTML document string.
        """
        styles = ""
        if self.include_styles:
            styles = f"<style>\n{self.style_manager.get_styles()}\n</style>"

        safe_title = html.escape(title, quote=True)
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="generator" content="md2html by Carlos Crespo">
    <title>{safe_title}</title>
    {styles}
</head>
<body>
    <article class="markdown-body">
        {toc_html}
        <main class="content">
            {body_content}
        </main>
    </article>
</body>
</html>"""

    def _escape_code_html(self, text: str) -> str:
        """
        Escape HTML special characters in code blocks.

        Args:
            text: Raw code text.

        Returns:
            HTML-escaped code text.
        """
        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace(">", "&gt;")
        text = text.replace('"', "&quot;")
        return text

    def _strip_html_tags(self, text: str) -> str:
        """
        Remove HTML tags from text.

        Used for creating clean TOC entries from header content
        that may contain inline HTML (bold, italic, etc.).

        Args:
            text: Text potentially containing HTML tags.

        Returns:
            Plain text with HTML tags removed.
        """
        import re

        return re.sub(r"<[^>]+>", "", text)


def convert_markdown_to_html(
    markdown_text: str,
    title: str = "Document",
    theme: Theme = Theme.LIGHT,
    include_toc: bool = True,
) -> str:
    """
    Convenience function to convert Markdown to HTML in one step.

    Args:
        markdown_text: Raw Markdown text to convert.
        title: HTML document title.
        theme: Color theme (LIGHT or DARK).
        include_toc: Whether to include table of contents.

    Returns:
        Complete HTML document string.

    Example:
        >>> md = "# Hello\\n\\nThis is **bold** text."
        >>> html = convert_markdown_to_html(md, title="My Doc")
    """
    parser = MarkdownParser()
    tokens = parser.parse(markdown_text)
    headers = parser.get_headers()

    converter = HTMLConverter(theme=theme, include_toc=include_toc)

    return converter.convert(tokens, title=title, headers=headers)
