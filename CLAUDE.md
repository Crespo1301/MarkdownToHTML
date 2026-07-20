# CLAUDE.md

Repo role: active public webapp and CLI tool featured in Portfolio as `Markdown to HTML Converter`.

## Business Context

- This repo is a public showcase web app and developer tool.
- Shared workflow rules live in `/home/cresp3/Portfolio/AI-WORKFLOW.md`.

## Claude Role Here

- Use Claude for product framing, landing-page clarity, docs readability, and UI critique.
- Let Codex handle Python implementation, testing, bug fixes, release prep, and GitHub closeout.

## Working Notes

- Python project with a CLI and a web interface.
- Keep README, demo flow, and tool messaging aligned with actual behavior.

## Useful Commands

```bash
bash ./scripts/stitch-doctor.sh
bash ./scripts/stitch-proxy.sh
bash ./scripts/magic-mcp.sh
```

## Shared AI Tooling

- Follow `AI-WORKFLOW.md` for the shared CSolutions AI stack.
- Use repo-local `.claude/skills/` for `code-review-graph`, `Impeccable`, and `mattpocock/skills` workflows.
- Use `.mcp.json` with `code-review-graph` after running `code-review-graph build` so exploration and reviews stay token-efficient.
- Use OpenSpec for larger changes that benefit from proposal, spec, and task artifacts.

## Visual QA

Use the workspace runner at `/home/cresp3/scripts/visual-check.sh` after any layout, responsive, spacing, animation, or visual-polish change. Start the local dev server, capture mobile and desktop screenshots into `.visual-checks/`, and inspect the rendered pixels before calling the work done. See `VISUAL-QA.md`.
