"""Regression tests for untrusted Markdown and generated document safety."""

from md2html.converter import convert_markdown_to_html


def test_document_title_is_escaped():
    output = convert_markdown_to_html("# Safe", title="</title><script>alert(1)</script>")
    assert "<script>" not in output
    assert "&lt;/title&gt;" in output


def test_javascript_link_is_not_rendered_as_anchor():
    output = convert_markdown_to_html("[click](javascript:alert(1))", include_toc=False)
    assert "javascript:" not in output
    assert "<a " not in output


def test_data_image_is_not_rendered():
    output = convert_markdown_to_html("![x](data:image/svg+xml,<svg/onload=alert(1)>)", include_toc=False)
    assert "data:image" not in output
    assert "<img" not in output


def test_attribute_quotes_are_escaped():
    output = convert_markdown_to_html(
        '[safe](https://example.com "quote &quot; onmouseover=&quot;alert(1)")',
        include_toc=False,
    )
    assert ' onmouseover="' not in output
    assert "&amp;quot;" in output


def test_safe_external_links_include_rel_protection():
    output = convert_markdown_to_html("[site](https://example.com)", include_toc=False)
    assert 'rel="noopener noreferrer"' in output


def test_code_language_cannot_inject_an_attribute():
    output = convert_markdown_to_html('```python" autofocus\nprint(1)\n```', include_toc=False)
    assert "autofocus" not in output
    assert 'class="language-python"' in output
