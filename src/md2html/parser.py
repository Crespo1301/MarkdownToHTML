"""
Markdown Parser Module

This module provides the MarkdownParser class that handles parsing of Markdown
syntax into structured tokens for HTML conversion.

Supported Markdown Syntax:
    - Headers (h1-h6): # through ######
    - Bold: **text** or __text__
    - Italic: *text* or _text_
    - Bold + Italic: ***text*** or ___text___
    - Links: [text](url) or [text](url "title")
    - Images: ![alt](src) or ![alt](src "title")
    - Unordered lists: -, *, or +
    - Ordered lists: 1., 2., etc.
    - Inline code: `code`
    - Code blocks: ``` or indented 4 spaces
    - Blockquotes: > text
    - Horizontal rules: ---, ***, or ___
    - Line breaks: two trailing spaces or <br>

Author: Carlos Crespo
"""

import html
import re
from urllib.parse import urlsplit
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, Tuple


class TokenType(Enum):
    """Enumeration of all supported Markdown token types."""
    
    HEADER = auto()
    PARAGRAPH = auto()
    BOLD = auto()
    ITALIC = auto()
    BOLD_ITALIC = auto()
    LINK = auto()
    IMAGE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()
    LIST_ITEM = auto()
    CODE_INLINE = auto()
    CODE_BLOCK = auto()
    BLOCKQUOTE = auto()
    HORIZONTAL_RULE = auto()
    LINE_BREAK = auto()
    TEXT = auto()
    NEWLINE = auto()


@dataclass
class Token:
    """
    Represents a parsed Markdown token.
    
    Attributes:
        type: The TokenType indicating what kind of Markdown element this is.
        content: The text content of the token.
        level: For headers (1-6), list nesting level, or blockquote depth.
        url: For links and images, the target URL.
        title: Optional title attribute for links and images.
        alt: For images, the alt text.
        language: For code blocks, the language identifier.
        children: Nested tokens for complex structures.
        id: Auto-generated ID for headers (used in TOC).
    """
    
    type: TokenType
    content: str = ""
    level: int = 0
    url: str = ""
    title: str = ""
    alt: str = ""
    language: str = ""
    children: List['Token'] = field(default_factory=list)
    id: str = ""


class MarkdownParser:
    """
    A comprehensive Markdown parser that converts Markdown text into tokens.
    
    The parser processes Markdown text in two phases:
    1. Block-level parsing: Headers, lists, code blocks, blockquotes, paragraphs
    2. Inline parsing: Bold, italic, links, images, inline code
    
    Example:
        >>> parser = MarkdownParser()
        >>> tokens = parser.parse("# Hello World\\n\\nThis is **bold** text.")
        >>> for token in tokens:
        ...     print(token.type, token.content)
    """
    
    # Regex patterns for block-level elements
    PATTERNS = {
        # Headers: # to ###### at start of line
        'header': re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE),
        
        # Horizontal rules: 3+ of -, *, or _ (with optional spaces)
        'hr': re.compile(r'^(?:[-*_]\s*){3,}$', re.MULTILINE),
        
        # Code blocks: ``` with optional language
        'code_block_fence': re.compile(
            r'^```(\w*)\n(.*?)^```',
            re.MULTILINE | re.DOTALL
        ),
        
        # Indented code blocks: 4 spaces or 1 tab
        'code_block_indent': re.compile(r'^(?:    |\t)(.+)$', re.MULTILINE),
        
        # Blockquotes: > at start (can be nested)
        'blockquote': re.compile(r'^(>+)\s*(.*)$', re.MULTILINE),
        
        # Unordered list items: -, *, or + followed by space
        'ul_item': re.compile(r'^(\s*)([-*+])\s+(.+)$', re.MULTILINE),
        
        # Ordered list items: number followed by . or )
        'ol_item': re.compile(r'^(\s*)(\d+)[.)]\s+(.+)$', re.MULTILINE),
        
        # Empty lines
        'empty_line': re.compile(r'^\s*$', re.MULTILINE),
    }
    
    # Regex patterns for inline elements
    INLINE_PATTERNS = {
        # Bold + Italic: ***text*** or ___text___
        'bold_italic': re.compile(r'(\*{3}|_{3})(?!\s)(.+?)(?<!\s)\1'),
        
        # Bold: **text** or __text__
        'bold': re.compile(r'(\*{2}|_{2})(?!\s)(.+?)(?<!\s)\1'),
        
        # Italic: *text* or _text_ (not preceded/followed by same char)
        'italic': re.compile(r'(?<![*_])(\*|_)(?!\s)(.+?)(?<!\s)\1(?![*_])'),
        
        # Images: ![alt](url) or ![alt](url "title")
        'image': re.compile(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)'),
        
        # Links: [text](url) or [text](url "title")
        'link': re.compile(r'(?<!!)\[([^\]]+)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)'),
        
        # Inline code: `code` (not ``)
        'code_inline': re.compile(r'(?<!`)`(?!`)([^`]+)`(?!`)'),
        
        # Line break: two or more trailing spaces
        'line_break': re.compile(r'  +\n'),
    }
    
    def __init__(self):
        """Initialize the parser with empty state."""
        self._tokens: List[Token] = []
        self._headers: List[Token] = []  # Track headers for TOC generation
    
    def parse(self, markdown_text: str) -> List[Token]:
        """
        Parse Markdown text into a list of tokens.
        
        Args:
            markdown_text: The raw Markdown string to parse.
            
        Returns:
            A list of Token objects representing the parsed content.
        """
        self._tokens = []
        self._headers = []
        
        # Normalize line endings
        text = markdown_text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Process block-level elements
        self._parse_blocks(text)
        
        return self._tokens
    
    def get_headers(self) -> List[Token]:
        """
        Get all headers found during parsing.
        
        Returns:
            A list of header tokens for TOC generation.
        """
        return self._headers
    
    def _parse_blocks(self, text: str) -> None:
        """
        Parse block-level Markdown elements.
        
        This method processes the text line by line, identifying block-level
        structures like headers, lists, code blocks, and blockquotes.
        
        Args:
            text: The Markdown text to parse.
        """
        lines = text.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Skip empty lines
            if self.PATTERNS['empty_line'].match(line):
                i += 1
                continue
            
            # Check for fenced code blocks
            if line.startswith('```'):
                i = self._parse_fenced_code_block(lines, i)
                continue
            
            # Check for headers
            header_match = self.PATTERNS['header'].match(line)
            if header_match:
                self._parse_header(header_match)
                i += 1
                continue
            
            # Check for horizontal rules
            if self.PATTERNS['hr'].match(line):
                self._tokens.append(Token(type=TokenType.HORIZONTAL_RULE))
                i += 1
                continue
            
            # Check for blockquotes
            blockquote_match = self.PATTERNS['blockquote'].match(line)
            if blockquote_match:
                i = self._parse_blockquote(lines, i)
                continue
            
            # Check for unordered lists
            ul_match = self.PATTERNS['ul_item'].match(line)
            if ul_match:
                i = self._parse_unordered_list(lines, i)
                continue
            
            # Check for ordered lists
            ol_match = self.PATTERNS['ol_item'].match(line)
            if ol_match:
                i = self._parse_ordered_list(lines, i)
                continue
            
            # Check for indented code blocks (4 spaces)
            if line.startswith('    ') or line.startswith('\t'):
                i = self._parse_indented_code_block(lines, i)
                continue
            
            # Default: treat as paragraph
            i = self._parse_paragraph(lines, i)
    
    def _parse_header(self, match: re.Match) -> None:
        """
        Parse a header line and create a header token.
        
        Args:
            match: Regex match object containing header hashes and text.
        """
        level = len(match.group(1))
        content = match.group(2).strip()
        
        # Generate slug for header ID
        header_id = self._generate_slug(content)
        
        # Parse inline elements in header content
        parsed_content = self._parse_inline(content)
        
        token = Token(
            type=TokenType.HEADER,
            content=parsed_content,
            level=level,
            id=header_id
        )
        
        self._tokens.append(token)
        self._headers.append(token)
    
    def _parse_paragraph(self, lines: List[str], start: int) -> int:
        """
        Parse a paragraph (continuous non-empty, non-special lines).
        
        Args:
            lines: All lines of the document.
            start: Starting line index.
            
        Returns:
            The index of the next line to process.
        """
        paragraph_lines = []
        i = start
        
        while i < len(lines):
            line = lines[i]
            
            # Empty line ends paragraph
            if self.PATTERNS['empty_line'].match(line):
                break
            
            # Special block elements end paragraph
            if (line.startswith('#') or 
                line.startswith('>') or
                line.startswith('```') or
                line.startswith('    ') or
                line.startswith('\t') or
                self.PATTERNS['hr'].match(line) or
                self.PATTERNS['ul_item'].match(line) or
                self.PATTERNS['ol_item'].match(line)):
                break
            
            paragraph_lines.append(line)
            i += 1
        
        if paragraph_lines:
            content = ' '.join(paragraph_lines)
            parsed_content = self._parse_inline(content)
            self._tokens.append(Token(
                type=TokenType.PARAGRAPH,
                content=parsed_content
            ))
        
        return i
    
    def _parse_fenced_code_block(self, lines: List[str], start: int) -> int:
        """
        Parse a fenced code block (``` ... ```).
        
        Args:
            lines: All lines of the document.
            start: Starting line index (at the opening ```).
            
        Returns:
            The index of the next line to process.
        """
        # Extract language from opening fence
        opening_line = lines[start]
        language = opening_line[3:].strip()
        
        code_lines = []
        i = start + 1
        
        while i < len(lines):
            if lines[i].startswith('```'):
                i += 1  # Skip closing fence
                break
            code_lines.append(lines[i])
            i += 1
        
        self._tokens.append(Token(
            type=TokenType.CODE_BLOCK,
            content='\n'.join(code_lines),
            language=language
        ))
        
        return i
    
    def _parse_indented_code_block(self, lines: List[str], start: int) -> int:
        """
        Parse an indented code block (4 spaces or tab).
        
        Args:
            lines: All lines of the document.
            start: Starting line index.
            
        Returns:
            The index of the next line to process.
        """
        code_lines = []
        i = start
        
        while i < len(lines):
            line = lines[i]
            
            # Continue if indented or empty (empty lines within code block)
            if line.startswith('    '):
                code_lines.append(line[4:])
                i += 1
            elif line.startswith('\t'):
                code_lines.append(line[1:])
                i += 1
            elif self.PATTERNS['empty_line'].match(line):
                # Check if next non-empty line is still indented
                j = i + 1
                while j < len(lines) and self.PATTERNS['empty_line'].match(lines[j]):
                    j += 1
                if j < len(lines) and (lines[j].startswith('    ') or lines[j].startswith('\t')):
                    code_lines.append('')
                    i += 1
                else:
                    break
            else:
                break
        
        self._tokens.append(Token(
            type=TokenType.CODE_BLOCK,
            content='\n'.join(code_lines)
        ))
        
        return i
    
    def _parse_blockquote(self, lines: List[str], start: int) -> int:
        """
        Parse a blockquote section.
        
        Args:
            lines: All lines of the document.
            start: Starting line index.
            
        Returns:
            The index of the next line to process.
        """
        quote_lines = []
        i = start
        
        while i < len(lines):
            line = lines[i]
            match = self.PATTERNS['blockquote'].match(line)
            
            if match:
                level = len(match.group(1))
                content = match.group(2)
                quote_lines.append((level, content))
                i += 1
            elif self.PATTERNS['empty_line'].match(line):
                # Check if blockquote continues after empty line
                if i + 1 < len(lines) and lines[i + 1].startswith('>'):
                    quote_lines.append((1, ''))
                    i += 1
                else:
                    break
            else:
                break
        
        # Combine quote lines and parse content
        content = '\n'.join(line[1] for line in quote_lines)
        parsed_content = self._parse_inline(content)
        
        self._tokens.append(Token(
            type=TokenType.BLOCKQUOTE,
            content=parsed_content,
            level=1
        ))
        
        return i
    
    def _parse_unordered_list(self, lines: List[str], start: int) -> int:
        """
        Parse an unordered list.
        
        Args:
            lines: All lines of the document.
            start: Starting line index.
            
        Returns:
            The index of the next line to process.
        """
        items = []
        i = start
        
        while i < len(lines):
            line = lines[i]
            match = self.PATTERNS['ul_item'].match(line)
            
            if match:
                indent = len(match.group(1))
                content = match.group(3)
                level = indent // 2  # 2 spaces per nesting level
                
                parsed_content = self._parse_inline(content)
                items.append(Token(
                    type=TokenType.LIST_ITEM,
                    content=parsed_content,
                    level=level
                ))
                i += 1
            elif self.PATTERNS['empty_line'].match(line):
                # Check if list continues
                if i + 1 < len(lines) and self.PATTERNS['ul_item'].match(lines[i + 1]):
                    i += 1
                else:
                    break
            else:
                break
        
        self._tokens.append(Token(
            type=TokenType.UNORDERED_LIST,
            children=items
        ))
        
        return i
    
    def _parse_ordered_list(self, lines: List[str], start: int) -> int:
        """
        Parse an ordered list.
        
        Args:
            lines: All lines of the document.
            start: Starting line index.
            
        Returns:
            The index of the next line to process.
        """
        items = []
        i = start
        
        while i < len(lines):
            line = lines[i]
            match = self.PATTERNS['ol_item'].match(line)
            
            if match:
                indent = len(match.group(1))
                content = match.group(3)
                level = indent // 2
                
                parsed_content = self._parse_inline(content)
                items.append(Token(
                    type=TokenType.LIST_ITEM,
                    content=parsed_content,
                    level=level
                ))
                i += 1
            elif self.PATTERNS['empty_line'].match(line):
                # Check if list continues
                if i + 1 < len(lines) and self.PATTERNS['ol_item'].match(lines[i + 1]):
                    i += 1
                else:
                    break
            else:
                break
        
        self._tokens.append(Token(
            type=TokenType.ORDERED_LIST,
            children=items
        ))
        
        return i
    
    def _parse_inline(self, text: str) -> str:
        """
        Parse inline Markdown elements and convert to HTML.
        
        This method handles bold, italic, links, images, and inline code.
        The order of processing matters to avoid conflicts.
        
        Args:
            text: The text to parse for inline elements.
            
        Returns:
            HTML string with inline elements converted.
        """
        if not text:
            return text
        
        # Process in specific order to avoid conflicts
        
        # 1. Escape HTML special characters first (but preserve our markers)
        text = self._escape_html(text)
        
        # 2. Process images before links (images start with !)
        text = self.INLINE_PATTERNS['image'].sub(
            self._replace_image, text
        )
        
        # 3. Process links
        text = self.INLINE_PATTERNS['link'].sub(
            self._replace_link, text
        )
        
        # 4. Process inline code (before bold/italic to preserve formatting)
        text = self.INLINE_PATTERNS['code_inline'].sub(
            r'<code>\1</code>', text
        )
        
        # 5. Process bold + italic (*** or ___)
        text = self.INLINE_PATTERNS['bold_italic'].sub(
            r'<strong><em>\2</em></strong>', text
        )
        
        # 6. Process bold (** or __)
        text = self.INLINE_PATTERNS['bold'].sub(
            r'<strong>\2</strong>', text
        )
        
        # 7. Process italic (* or _)
        text = self.INLINE_PATTERNS['italic'].sub(
            r'<em>\2</em>', text
        )
        
        # 8. Process line breaks
        text = self.INLINE_PATTERNS['line_break'].sub(
            '<br>\n', text
        )
        
        return text
    
    def _replace_link(self, match: re.Match) -> str:
        """
        Replace a link match with HTML anchor tag.
        
        Args:
            match: Regex match object with groups (text, url, title).
            
        Returns:
            HTML anchor tag string.
        """
        text = match.group(1)
        url = self._sanitize_url(match.group(2), image=False)
        title = match.group(3)

        if url is None:
            return text
        
        if title:
            safe_title = html.escape(html.unescape(title), quote=True)
            return f'<a href="{url}" title="{safe_title}" rel="noopener noreferrer">{text}</a>'
        return f'<a href="{url}" rel="noopener noreferrer">{text}</a>'
    
    def _replace_image(self, match: re.Match) -> str:
        """
        Replace an image match with HTML img tag.
        
        Args:
            match: Regex match object with groups (alt, src, title).
            
        Returns:
            HTML img tag string.
        """
        alt = html.escape(html.unescape(match.group(1)), quote=True)
        src = self._sanitize_url(match.group(2), image=True)
        title = match.group(3)

        if src is None:
            return alt
        
        if title:
            safe_title = html.escape(html.unescape(title), quote=True)
            return f'<img src="{src}" alt="{alt}" title="{safe_title}">'
        return f'<img src="{src}" alt="{alt}">'

    @staticmethod
    def _sanitize_url(raw_url: str, image: bool) -> Optional[str]:
        """Return an attribute-safe URL or ``None`` for unsafe schemes."""
        decoded = html.unescape(raw_url).strip()
        if any(ord(character) < 32 for character in decoded):
            return None

        parsed = urlsplit(decoded)
        scheme = parsed.scheme.lower()
        allowed_schemes = {"http", "https"} if image else {"http", "https", "mailto"}
        if scheme and scheme not in allowed_schemes:
            return None
        if decoded.startswith("//"):
            return None
        return html.escape(decoded, quote=True)
    
    def _escape_html(self, text: str) -> str:
        """
        Escape HTML special characters.
        
        Args:
            text: Raw text that may contain HTML special chars.
            
        Returns:
            Text with &, <, >, ", ' escaped.
        """
        # Only escape if not already inside our inline patterns
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        return text
    
    def _generate_slug(self, text: str) -> str:
        """
        Generate a URL-friendly slug from header text.
        
        Args:
            text: The header text to slugify.
            
        Returns:
            A lowercase, hyphenated slug suitable for HTML IDs.
        """
        # Remove any inline markdown/HTML
        slug = re.sub(r'[*_`\[\]()!]', '', text)
        
        # Convert to lowercase
        slug = slug.lower()
        
        # Replace spaces and special chars with hyphens
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        
        return slug or 'section'


# Convenience function for quick parsing
def parse_markdown(text: str) -> List[Token]:
    """
    Convenience function to parse Markdown text.
    
    Args:
        text: Markdown text to parse.
        
    Returns:
        List of parsed tokens.
        
    Example:
        >>> tokens = parse_markdown("# Hello\\n\\nWorld")
    """
    parser = MarkdownParser()
    return parser.parse(text)
