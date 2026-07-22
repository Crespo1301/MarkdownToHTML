# Claude and Codex track record

## 2026-07-22: v2.1.0 functionality, security, and content pass

- Source: Docs (user-approved full-pass brief covering design, functionality,
  security, accessibility, SEO/AEO, AdSense-readiness, and release)
- Target: parser (ReDoS fix, unique heading IDs, hard line breaks, inline
  code protection, nested/fragment TOC), API (fragment TOC wiring, wall-clock
  timeout guard, narrowed AdSense CSP), and the converter UI (stale-output
  invalidation, tab keyboard navigation, reduced per-keystroke work)
- Direction: fix the functional/security defects found during review rather
  than rewriting the parser or the mobile layout; keep the zero-dependency
  parser; defer the larger "Editor/Preview/Source mode switch" mobile
  redesign to a dedicated design pass instead of bundling it into a
  correctness-and-security release
- Status: accepted
- Claude implementation: found and fixed the ReDoS via direct timing
  reproduction, rewrote TOC generation as a tree-based renderer, added
  code-span protection and hard-line-break handling in the parser, narrowed
  the AdSense CSP against a researched Google host list, added roving-
  tabindex keyboard navigation to the output tabs, added 24 regression
  tests, added a real `.flake8` config (vanilla flake8 was silently
  ignoring `pyproject.toml`), reformatted the whole codebase with black,
  and updated README/CHANGELOG/HANDOFF/ADSENSE docs for accuracy
- Release: v2.1.0

## 2026-07-21: public converter 2.0

- Source: Docs (user-approved release brief)
- Target: converter, security baseline, discovery content, and domain readiness
- Direction: keep the working tool first; use a restrained professional utility
  interface; avoid marketing-first layout and decorative effects
- Status: accepted
- Codex implementation: secure output generation and API validation, sandboxed
  preview, product workflow rebuild, legal/discovery pages, crawler files,
  AdSense preparation, documentation, tests, visual QA, and release closeout
- Release: v2.0.0
