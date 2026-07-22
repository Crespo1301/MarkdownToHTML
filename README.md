# Markdown to HTML Converter

A secure, zero-runtime-dependency Python CLI/library and free web converter for
turning Markdown into an HTML fragment or a complete styled document.

- Production URL (after DNS launch): <https://mdtohtmlconverter.com>
- Current Vercel URL: <https://markdown-to-html-iota.vercel.app>
- Version: `2.0.0`

## Web converter

The converter is the first screen. It includes:

- Markdown input, sandboxed rendered preview, and raw HTML source
- Copy HTML and download-complete-document actions
- `.md`, `.markdown`, and `.txt` upload with a 750 KB limit
- clear and sample controls
- light and dark output themes
- optional table of contents
- fragment and complete-document output modes
- character, word, and line counts
- abortable conversion requests that prevent stale results
- local browser draft recovery
- keyboard labels, live status, visible focus, and responsive layouts

Markdown is sent to a serverless API for conversion. The application has no
document database and does not intentionally store submitted document content.
Browser draft recovery uses local storage on the user's device.

## Supported Markdown

The parser supports:

- headings (levels 1 through 6)
- bold, italic, and combined emphasis
- safe HTTP, HTTPS, mailto, relative, and fragment links
- HTTP, HTTPS, and relative images
- ordered and unordered lists
- fenced and indented code blocks
- inline code, blockquotes, horizontal rules, and paragraphs

Raw HTML is escaped. Unsafe schemes such as `javascript:` and `data:` are not
rendered as active links or images. Extended syntax including tables, task
lists, and strikethrough is not currently interpreted.

## Install and use the CLI

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
md2html README.md
md2html README.md --theme dark --no-toc
md2html README.md --fragment -o readme-fragment.html
```

Run without installing:

```bash
PYTHONPATH=src python -m md2html.cli README.md --dry-run
```

## Python API

```python
from md2html.converter import convert_markdown_to_html
from md2html.styles import Theme

html = convert_markdown_to_html(
    "# Hello\n\nA **safe** document.",
    title="Example",
    theme=Theme.LIGHT,
    include_toc=True,
)
```

## Local web development

The production entry point uses Python's `BaseHTTPRequestHandler`, so no Flask
runtime is required.

```bash
vercel dev
```

The API accepts `POST /api/convert` with `application/json`:

```json
{
  "markdown": "# Hello",
  "title": "Example",
  "theme": "light",
  "includeToc": true,
  "fragmentOnly": false
}
```

Request bodies are limited to 1 MB. Markdown is limited to 750,000 characters
and titles to 200 characters.

## Test and verify

```bash
source venv/bin/activate
pytest
git diff --check
code-review-graph build
```

For visual changes, start the real local server and use the shared runner:

```bash
/home/cresp3/scripts/visual-check.sh --url http://localhost:3000/ --out .visual-checks/mobile.png
/home/cresp3/scripts/visual-check.sh --desktop --url http://localhost:3000/ --out .visual-checks/desktop.png
```

## Security model

- all Markdown HTML special characters are escaped
- generated title and attribute values are escaped
- URL schemes are allowlisted
- preview uses a sandboxed iframe without script permissions
- API content type, JSON shape, field types, and sizes are validated
- static file paths are resolved inside the static directory
- public errors do not reveal exception details
- CSP, framing, content-type, referrer, and permissions headers are applied
- conversion responses use `Cache-Control: no-store`

See [SECURITY-CHECKLIST.md](SECURITY-CHECKLIST.md) and
[HANDOFF.md](HANDOFF.md) for the release audit and operational notes.

## Project structure

```text
api/index.py          Vercel HTTP entry point
src/md2html/          Python parser, converter, styles, and CLI
static/               Browser CSS, JavaScript, crawler files, and images
templates/            Tool, legal, support, and 404 pages
tests/                Parser, converter, API, and security tests
examples/             Example Markdown inputs
```

## License and author

MIT License. Built by [Carlos Crespo](https://carloscrespo.info) as a public
[CSolutions](https://carloscrespo.info) utility. Contributions and issue reports
are welcome in the [GitHub repository](https://github.com/Crespo1301/MarkdownToHTML).
