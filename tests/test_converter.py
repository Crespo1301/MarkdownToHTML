"""
Unit Tests for HTML Converter

Tests HTML generation, table of contents creation, theming,
and document structure.

Run with: pytest tests/test_converter.py -v
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from md2html.parser import MarkdownParser
from md2html.converter import HTMLConverter, convert_markdown_to_html
from md2html.styles import Theme


class TestHTMLGeneration:
    """Test suite for basic HTML generation."""

    @pytest.fixture
    def parser(self):
        return MarkdownParser()

    @pytest.fixture
    def converter(self):
        return HTMLConverter(include_toc=False)

    def test_header_conversion(self, parser, converter):
        """Test header is converted to HTML heading."""
        tokens = parser.parse("# Hello World")
        html = converter.convert(tokens, title="Test")
        assert "<h1" in html
        assert "Hello World" in html
        assert 'id="hello-world"' in html

    def test_paragraph_conversion(self, parser, converter):
        """Test paragraph is wrapped in <p> tags."""
        tokens = parser.parse("This is a paragraph.")
        html = converter.convert(tokens, title="Test")
        assert "<p>This is a paragraph.</p>" in html

    def test_code_block_conversion(self, parser, converter):
        """Test code block is wrapped in <pre><code> tags."""
        md = """```python
print("hello")
```"""
        tokens = parser.parse(md)
        html = converter.convert(tokens, title="Test")
        assert "<pre>" in html
        assert "<code" in html
        assert 'class="language-python"' in html

    def test_unordered_list_conversion(self, parser, converter):
        """Test unordered list generates <ul><li> structure."""
        md = """- Item 1
- Item 2"""
        tokens = parser.parse(md)
        html = converter.convert(tokens, title="Test")
        assert "<ul>" in html
        assert "<li>" in html
        assert "Item 1" in html

    def test_ordered_list_conversion(self, parser, converter):
        """Test ordered list generates <ol><li> structure."""
        md = """1. First
2. Second"""
        tokens = parser.parse(md)
        html = converter.convert(tokens, title="Test")
        assert "<ol>" in html
        assert "<li>" in html

    def test_blockquote_conversion(self, parser, converter):
        """Test blockquote generates <blockquote> tag."""
        tokens = parser.parse("> Quote here")
        html = converter.convert(tokens, title="Test")
        assert "<blockquote>" in html

    def test_horizontal_rule_conversion(self, parser, converter):
        """Test horizontal rule generates <hr> tag."""
        tokens = parser.parse("---")
        html = converter.convert(tokens, title="Test")
        assert "<hr>" in html


class TestDocumentStructure:
    """Test suite for complete document structure."""

    def test_has_doctype(self):
        """Test output includes DOCTYPE declaration."""
        html = convert_markdown_to_html("# Test", include_toc=False)
        assert "<!DOCTYPE html>" in html

    def test_has_html_lang(self):
        """Test output includes html lang attribute."""
        html = convert_markdown_to_html("# Test", include_toc=False)
        assert '<html lang="en">' in html

    def test_has_meta_charset(self):
        """Test output includes charset meta tag."""
        html = convert_markdown_to_html("# Test", include_toc=False)
        assert 'charset="UTF-8"' in html

    def test_has_viewport_meta(self):
        """Test output includes viewport meta tag."""
        html = convert_markdown_to_html("# Test", include_toc=False)
        assert "viewport" in html

    def test_has_title(self):
        """Test output includes document title."""
        html = convert_markdown_to_html(
            "# Test", title="My Document", include_toc=False
        )
        assert "<title>My Document</title>" in html

    def test_has_body(self):
        """Test output includes body tag."""
        html = convert_markdown_to_html("# Test", include_toc=False)
        assert "<body>" in html
        assert "</body>" in html

    def test_has_markdown_body_class(self):
        """Test output includes markdown-body container."""
        html = convert_markdown_to_html("# Test", include_toc=False)
        assert 'class="markdown-body"' in html


class TestTableOfContents:
    """Test suite for table of contents generation."""

    def test_toc_generated_by_default(self):
        """Test TOC is generated when headers are present."""
        md = """# Title

## Section 1

## Section 2"""
        html = convert_markdown_to_html(md, include_toc=True)
        assert 'class="toc"' in html

    def test_toc_contains_header_links(self):
        """Test TOC contains links to headers."""
        md = """# Main Title

## First Section

## Second Section"""
        html = convert_markdown_to_html(md, include_toc=True)
        assert 'href="#first-section"' in html
        assert 'href="#second-section"' in html

    def test_toc_respects_title_option(self):
        """Test custom TOC title is used."""
        converter = HTMLConverter(include_toc=True, toc_title="Contents")
        parser = MarkdownParser()
        tokens = parser.parse("# Heading")
        html = converter.convert(tokens, title="Test", headers=parser.get_headers())
        assert "Contents" in html

    def test_no_toc_when_disabled(self):
        """Test TOC is not generated when disabled."""
        html = convert_markdown_to_html("# Test", include_toc=False)
        assert 'class="toc"' not in html

    def test_no_toc_without_headers(self):
        """Test no TOC when document has no headers."""
        html = convert_markdown_to_html("Just a paragraph.", include_toc=True)
        # Should not have TOC since there are no headers
        assert 'class="toc-list"' not in html


class TestTheming:
    """Test suite for theme support."""

    def test_light_theme_default(self):
        """Test light theme is default."""
        html = convert_markdown_to_html("# Test", theme=Theme.LIGHT)
        # Light theme uses white background
        assert "#ffffff" in html or "bg_primary" in html

    def test_dark_theme_colors(self):
        """Test dark theme uses dark colors."""
        html = convert_markdown_to_html("# Test", theme=Theme.DARK)
        # Dark theme uses dark background
        assert "#0d1117" in html

    def test_styles_included_by_default(self):
        """Test CSS styles are embedded by default."""
        converter = HTMLConverter(include_styles=True)
        parser = MarkdownParser()
        tokens = parser.parse("# Test")
        html = converter.convert(tokens, title="Test")
        assert "<style>" in html

    def test_styles_excluded_when_disabled(self):
        """Test styles can be excluded."""
        converter = HTMLConverter(include_styles=False)
        parser = MarkdownParser()
        tokens = parser.parse("# Test")
        html = converter.convert(tokens, title="Test")
        assert "<style>" not in html


class TestFragmentMode:
    """Test suite for HTML fragment generation."""

    def test_fragment_no_html_wrapper(self):
        """Test fragment mode doesn't include html/head/body."""
        converter = HTMLConverter()
        parser = MarkdownParser()
        tokens = parser.parse("# Hello")
        fragment = converter.convert_fragment(tokens)

        assert "<!DOCTYPE" not in fragment
        assert "<html" not in fragment
        assert "<head" not in fragment
        assert "<body" not in fragment

    def test_fragment_contains_content(self):
        """Test fragment contains converted content."""
        converter = HTMLConverter()
        parser = MarkdownParser()
        tokens = parser.parse("# Hello\n\nWorld")
        fragment = converter.convert_fragment(tokens)

        assert "<h1" in fragment
        assert "Hello" in fragment
        assert "<p>" in fragment


class TestCodeBlockEscaping:
    """Test suite for HTML escaping in code blocks."""

    def test_code_escapes_html(self):
        """Test that HTML in code blocks is escaped."""
        md = """```html
<div class="test">Content</div>
```"""
        html = convert_markdown_to_html(md, include_toc=False)
        assert "&lt;div" in html
        assert "&gt;" in html

    def test_code_escapes_ampersand(self):
        """Test that & in code is escaped."""
        md = """```
x && y
```"""
        html = convert_markdown_to_html(md, include_toc=False)
        assert "&amp;&amp;" in html


class TestConvenienceFunction:
    """Test suite for the convert_markdown_to_html function."""

    def test_basic_conversion(self):
        """Test basic conversion with convenience function."""
        html = convert_markdown_to_html("# Hello")
        assert "<h1" in html
        assert "Hello" in html

    def test_all_options(self):
        """Test all options can be passed."""
        html = convert_markdown_to_html(
            "# Test", title="Custom Title", theme=Theme.DARK, include_toc=False
        )
        assert "<title>Custom Title</title>" in html
        assert "#0d1117" in html  # Dark theme color


class TestEdgeCases:
    """Test suite for edge cases."""

    def test_empty_tokens(self):
        """Test converter handles empty token list."""
        converter = HTMLConverter()
        html = converter.convert([], title="Empty")
        assert "<!DOCTYPE html>" in html

    def test_special_characters_in_title(self):
        """Test special characters in document title."""
        html = convert_markdown_to_html(
            "# Test", title="Tom & Jerry's <Adventure>", include_toc=False
        )
        assert "Tom &amp; Jerry&#x27;s &lt;Adventure&gt;" in html


class TestNestedTableOfContents:
    """Regression tests: TOC nesting must produce valid, well-formed HTML."""

    def test_deeper_header_nests_ul_inside_the_parent_li(self):
        md = "# Title\n\n## Section\n\n### Subsection"
        html = convert_markdown_to_html(md, include_toc=True)
        toc = html.split('<nav class="toc">', 1)[1].split("</nav>", 1)[0]
        # A nested <ul> must be a child of the <li> above it, never a
        # direct sibling of another <ul> (which is invalid HTML).
        assert "<li>" in toc
        title_li_start = toc.index("<li>")
        nested_ul_start = toc.index("<ul>", toc.index("Section"))
        closing_li_after_nested = toc.index("</li>", nested_ul_start)
        assert title_li_start < nested_ul_start < closing_li_after_nested

    def test_level_jump_from_h1_to_h3_does_not_break_nesting(self):
        # No h2 in between; the h3 should still nest under the h1 rather
        # than producing sibling <ul> tags with no wrapping <li>.
        md = "# Title\n\n### Deep section"
        html = convert_markdown_to_html(md, include_toc=True)
        toc = html.split('<nav class="toc">', 1)[1].split("</nav>", 1)[0]
        assert "<ul><ul>" not in toc.replace("\n", "")
        assert toc.count("<a href=") == 2

    def test_sibling_headers_at_same_level_stay_flat(self):
        md = "## One\n\n## Two\n\n## Three"
        html = convert_markdown_to_html(md, include_toc=True)
        toc = html.split('<nav class="toc">', 1)[1].split("</nav>", 1)[0]
        assert toc.count("<ul") == 1
        assert toc.count("<a href=") == 3

    def test_returning_to_a_shallower_level_closes_nested_lists(self):
        md = "# A\n\n## A1\n\n## A2\n\n# B"
        html = convert_markdown_to_html(md, include_toc=True)
        toc = html.split('<nav class="toc">', 1)[1].split("</nav>", 1)[0]
        # Balanced tags: every opened <ul>/<li> is closed.
        assert toc.count("<ul") == toc.count("</ul>")
        assert toc.count("<li>") == toc.count("</li>")


class TestFragmentTableOfContents:
    """Regression tests: fragment mode must not silently ignore include_toc."""

    def test_fragment_includes_toc_when_enabled(self):
        parser = MarkdownParser()
        md = "# Title\n\nBody text.\n\n## Section"
        tokens = parser.parse(md)
        headers = parser.get_headers()
        converter = HTMLConverter(include_toc=True, include_styles=False)
        fragment = converter.convert_fragment(tokens, headers=headers)
        assert 'class="toc"' in fragment
        assert "<!DOCTYPE" not in fragment
        assert "<body" not in fragment

    def test_fragment_omits_toc_when_disabled(self):
        parser = MarkdownParser()
        tokens = parser.parse("# Title\n\nBody text.")
        headers = parser.get_headers()
        converter = HTMLConverter(include_toc=False, include_styles=False)
        fragment = converter.convert_fragment(tokens, headers=headers)
        assert 'class="toc"' not in fragment

    def test_fragment_omits_toc_when_no_headers_present(self):
        parser = MarkdownParser()
        tokens = parser.parse("Just a paragraph, no headers.")
        headers = parser.get_headers()
        converter = HTMLConverter(include_toc=True, include_styles=False)
        fragment = converter.convert_fragment(tokens, headers=headers)
        assert 'class="toc"' not in fragment


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
