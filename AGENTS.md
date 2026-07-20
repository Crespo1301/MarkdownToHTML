# AGENTS.md

Guidance for Codex and Claude when working in this repository.

## Repo Role

MarkdownToHTML is a public CSolutions utility and showcase project. It ships a
Python CLI/library and a small web/API surface for converting Markdown to styled
HTML.

## Project Shape

- Python package source lives in `src/md2html/`.
- Tests live in `tests/`.
- Demo inputs live in `examples/`.
- Generated HTML belongs in `output/` and should stay untracked except for
  `output/.gitkeep`.
- Vercel API entrypoint lives in `api/index.py`.

## Commands

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest
git diff --check
```

For a lighter local install:

```bash
pip install -e .
PYTHONPATH=src python -m md2html.cli README.md --dry-run
```

## Working Rules

- Keep README claims aligned with the actual CLI, parser, and web/API behavior.
- Update tests and examples when changing Markdown parsing or HTML output.
- Keep `.mcp.json`, `.env.ai.local`, virtual environments, caches, generated
  HTML output, and copied skill folders local-only.
- Treat `*:Zone.Identifier` files as Windows metadata artifacts, not project
  source.
- Do not commit secrets or machine-local credentials.

## Visual QA

Use the workspace runner at `/home/cresp3/scripts/visual-check.sh` after any layout, responsive, spacing, animation, or visual-polish change. Start the local dev server, capture mobile and desktop screenshots into `.visual-checks/`, and inspect the rendered pixels before calling the work done. See `VISUAL-QA.md`.
