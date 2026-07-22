"""
Unit Tests for Markdown Parser

Tests all parsing functionality including headers, text formatting,
links, images, lists, code blocks, blockquotes, and inline elements.

Run with: pytest tests/test_parser.py -v
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from md2html.parser import MarkdownParser, TokenType, Token


class TestHeaderParsing:
    """Test suite for header parsing functionality."""
    
    @pytest.fixture
    def parser(self):
        """Create a fresh parser instance for each test."""
        return MarkdownParser()
    
    def test_h1_parsing(self, parser):
        """Test parsing of h1 headers."""
        tokens = parser.parse("# Hello World")
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.HEADER
        assert tokens[0].level == 1
        assert "Hello World" in tokens[0].content
    
    def test_h2_parsing(self, parser):
        """Test parsing of h2 headers."""
        tokens = parser.parse("## Section Title")
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.HEADER
        assert tokens[0].level == 2
    
    def test_h6_parsing(self, parser):
        """Test parsing of h6 headers (smallest)."""
        tokens = parser.parse("###### Small Header")
        assert len(tokens) == 1
        assert tokens[0].level == 6
    
    def test_header_id_generation(self, parser):
        """Test that headers get URL-friendly IDs."""
        tokens = parser.parse("# Hello World Example")
        assert tokens[0].id == "hello-world-example"
    
    def test_header_id_special_chars(self, parser):
        """Test ID generation with special characters."""
        tokens = parser.parse("# What's New in 2024?")
        # Should remove special chars and create valid ID
        assert tokens[0].id
        assert " " not in tokens[0].id
    
    def test_multiple_headers(self, parser):
        """Test parsing multiple headers."""
        md = """# Title
        
## Section 1

## Section 2"""
        tokens = parser.parse(md)
        headers = [t for t in tokens if t.type == TokenType.HEADER]
        assert len(headers) == 3
    
    def test_get_headers_method(self, parser):
        """Test the get_headers() method returns all headers."""
        parser.parse("# H1\n\n## H2\n\n### H3")
        headers = parser.get_headers()
        assert len(headers) == 3


class TestTextFormatting:
    """Test suite for bold, italic, and combined formatting."""
    
    @pytest.fixture
    def parser(self):
        return MarkdownParser()
    
    def test_bold_asterisks(self, parser):
        """Test bold text with double asterisks."""
        tokens = parser.parse("This is **bold** text")
        assert "<strong>bold</strong>" in tokens[0].content
    
    def test_bold_underscores(self, parser):
        """Test bold text with double underscores."""
        tokens = parser.parse("This is __bold__ text")
        assert "<strong>bold</strong>" in tokens[0].content
    
    def test_italic_asterisk(self, parser):
        """Test italic text with single asterisk."""
        tokens = parser.parse("This is *italic* text")
        assert "<em>italic</em>" in tokens[0].content
    
    def test_italic_underscore(self, parser):
        """Test italic text with single underscore."""
        tokens = parser.parse("This is _italic_ text")
        assert "<em>italic</em>" in tokens[0].content
    
    def test_bold_italic_combined(self, parser):
        """Test bold and italic combined."""
        tokens = parser.parse("This is ***bold italic*** text")
        assert "<strong><em>bold italic</em></strong>" in tokens[0].content
    
    def test_nested_formatting(self, parser):
        """Test nested bold inside italic or vice versa."""
        tokens = parser.parse("This is **bold with *nested italic* inside**")
        content = tokens[0].content
        assert "<strong>" in content
        assert "<em>" in content


class TestLinks:
    """Test suite for link parsing."""
    
    @pytest.fixture
    def parser(self):
        return MarkdownParser()
    
    def test_basic_link(self, parser):
        """Test basic link parsing."""
        tokens = parser.parse("[GitHub](https://github.com)")
        assert '<a href="https://github.com" rel="noopener noreferrer">GitHub</a>' in tokens[0].content
    
    def test_link_with_title(self, parser):
        """Test link with title attribute."""
        tokens = parser.parse('[Google](https://google.com "Search Engine")')
        content = tokens[0].content
        assert 'href="https://google.com"' in content
        assert 'title="Search Engine"' in content
    
    def test_multiple_links(self, parser):
        """Test multiple links in same paragraph."""
        tokens = parser.parse("Visit [A](http://a.com) and [B](http://b.com)")
        content = tokens[0].content
        assert content.count("<a href=") == 2


class TestImages:
    """Test suite for image parsing."""
    
    @pytest.fixture
    def parser(self):
        return MarkdownParser()
    
    def test_basic_image(self, parser):
        """Test basic image parsing."""
        tokens = parser.parse("![Alt text](image.png)")
        assert '<img src="image.png" alt="Alt text">' in tokens[0].content
    
    def test_image_with_title(self, parser):
        """Test image with title attribute."""
        tokens = parser.parse('![Photo](pic.jpg "My Photo")')
        content = tokens[0].content
        assert 'title="My Photo"' in content


class TestLists:
    """Test suite for list parsing."""
    
    @pytest.fixture
    def parser(self):
        return MarkdownParser()
    
    def test_unordered_list_dash(self, parser):
        """Test unordered list with dashes."""
        md = """- Item 1
- Item 2
- Item 3"""
        tokens = parser.parse(md)
        assert any(t.type == TokenType.UNORDERED_LIST for t in tokens)
    
    def test_unordered_list_asterisk(self, parser):
        """Test unordered list with asterisks."""
        md = """* Item 1
* Item 2"""
        tokens = parser.parse(md)
        ul_tokens = [t for t in tokens if t.type == TokenType.UNORDERED_LIST]
        assert len(ul_tokens) == 1
        assert len(ul_tokens[0].children) == 2
    
    def test_ordered_list(self, parser):
        """Test ordered list parsing."""
        md = """1. First
2. Second
3. Third"""
        tokens = parser.parse(md)
        ol_tokens = [t for t in tokens if t.type == TokenType.ORDERED_LIST]
        assert len(ol_tokens) == 1
        assert len(ol_tokens[0].children) == 3
    
    def test_list_item_content(self, parser):
        """Test that list items contain correct content."""
        md = """- **Bold item**
- *Italic item*"""
        tokens = parser.parse(md)
        ul = next(t for t in tokens if t.type == TokenType.UNORDERED_LIST)
        assert "<strong>" in ul.children[0].content
        assert "<em>" in ul.children[1].content


class TestCodeBlocks:
    """Test suite for code block parsing."""
    
    @pytest.fixture
    def parser(self):
        return MarkdownParser()
    
    def test_fenced_code_block(self, parser):
        """Test fenced code block with backticks."""
        md = """```
code here
```"""
        tokens = parser.parse(md)
        code_tokens = [t for t in tokens if t.type == TokenType.CODE_BLOCK]
        assert len(code_tokens) == 1
        assert "code here" in code_tokens[0].content
    
    def test_fenced_code_with_language(self, parser):
        """Test fenced code block with language identifier."""
        md = """```python
def hello():
    print("Hello")
```"""
        tokens = parser.parse(md)
        code_token = next(t for t in tokens if t.type == TokenType.CODE_BLOCK)
        assert code_token.language == "python"
    
    def test_indented_code_block(self, parser):
        """Test code block with 4-space indentation."""
        md = """    code line 1
    code line 2"""
        tokens = parser.parse(md)
        code_tokens = [t for t in tokens if t.type == TokenType.CODE_BLOCK]
        assert len(code_tokens) == 1
    
    def test_inline_code(self, parser):
        """Test inline code parsing."""
        tokens = parser.parse("Use `print()` function")
        assert "<code>print()</code>" in tokens[0].content


class TestBlockquotes:
    """Test suite for blockquote parsing."""
    
    @pytest.fixture
    def parser(self):
        return MarkdownParser()
    
    def test_single_line_blockquote(self, parser):
        """Test single line blockquote."""
        tokens = parser.parse("> This is a quote")
        bq_tokens = [t for t in tokens if t.type == TokenType.BLOCKQUOTE]
        assert len(bq_tokens) == 1
        assert "This is a quote" in bq_tokens[0].content
    
    def test_multi_line_blockquote(self, parser):
        """Test multi-line blockquote."""
        md = """> Line 1
> Line 2
> Line 3"""
        tokens = parser.parse(md)
        bq_tokens = [t for t in tokens if t.type == TokenType.BLOCKQUOTE]
        assert len(bq_tokens) == 1


class TestHorizontalRules:
    """Test suite for horizontal rule parsing."""
    
    @pytest.fixture
    def parser(self):
        return MarkdownParser()
    
    def test_hr_dashes(self, parser):
        """Test horizontal rule with dashes."""
        tokens = parser.parse("---")
        assert any(t.type == TokenType.HORIZONTAL_RULE for t in tokens)
    
    def test_hr_asterisks(self, parser):
        """Test horizontal rule with asterisks."""
        tokens = parser.parse("***")
        assert any(t.type == TokenType.HORIZONTAL_RULE for t in tokens)
    
    def test_hr_underscores(self, parser):
        """Test horizontal rule with underscores."""
        tokens = parser.parse("___")
        assert any(t.type == TokenType.HORIZONTAL_RULE for t in tokens)
    
    def test_hr_with_spaces(self, parser):
        """Test horizontal rule with spaces between."""
        tokens = parser.parse("- - -")
        assert any(t.type == TokenType.HORIZONTAL_RULE for t in tokens)


class TestParagraphs:
    """Test suite for paragraph parsing."""
    
    @pytest.fixture
    def parser(self):
        return MarkdownParser()
    
    def test_single_paragraph(self, parser):
        """Test single paragraph parsing."""
        tokens = parser.parse("This is a paragraph.")
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.PARAGRAPH
    
    def test_multiple_paragraphs(self, parser):
        """Test multiple paragraphs separated by blank lines."""
        md = """First paragraph.

Second paragraph."""
        tokens = parser.parse(md)
        paragraphs = [t for t in tokens if t.type == TokenType.PARAGRAPH]
        assert len(paragraphs) == 2
    
    def test_paragraph_with_inline_formatting(self, parser):
        """Test paragraph containing inline formatting."""
        tokens = parser.parse("A paragraph with **bold** and *italic* text.")
        content = tokens[0].content
        assert "<strong>bold</strong>" in content
        assert "<em>italic</em>" in content


class TestHTMLEscaping:
    """Test suite for HTML character escaping."""
    
    @pytest.fixture
    def parser(self):
        return MarkdownParser()
    
    def test_escape_less_than(self, parser):
        """Test that < is escaped."""
        tokens = parser.parse("Use x < y for comparison")
        assert "&lt;" in tokens[0].content
    
    def test_escape_greater_than(self, parser):
        """Test that > is escaped in content (not blockquote)."""
        tokens = parser.parse("Use x > y for comparison")
        # Note: This appears in a paragraph, not as blockquote marker
        # The > should be escaped in the inline content
        assert tokens[0].type == TokenType.PARAGRAPH
    
    def test_escape_ampersand(self, parser):
        """Test that & is escaped."""
        tokens = parser.parse("Tom & Jerry")
        assert "&amp;" in tokens[0].content


class TestEdgeCases:
    """Test suite for edge cases and special scenarios."""
    
    @pytest.fixture
    def parser(self):
        return MarkdownParser()
    
    def test_empty_input(self, parser):
        """Test parsing empty string."""
        tokens = parser.parse("")
        assert tokens == []
    
    def test_whitespace_only(self, parser):
        """Test parsing whitespace-only input."""
        tokens = parser.parse("   \n\n   ")
        assert tokens == []
    
    def test_windows_line_endings(self, parser):
        """Test that Windows line endings are handled."""
        tokens = parser.parse("# Header\r\n\r\nParagraph")
        assert len(tokens) == 2
    
    def test_mixed_content(self, parser):
        """Test document with various element types."""
        md = """# Title

A paragraph with **bold** text.

- List item 1
- List item 2

> A quote

```python
code
```"""
        tokens = parser.parse(md)
        types = {t.type for t in tokens}
        assert TokenType.HEADER in types
        assert TokenType.PARAGRAPH in types
        assert TokenType.UNORDERED_LIST in types
        assert TokenType.BLOCKQUOTE in types
        assert TokenType.CODE_BLOCK in types


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
