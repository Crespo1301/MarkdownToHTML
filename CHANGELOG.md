# Changelog

All notable changes follow semantic versioning.

## [2.2.0] - 2026-07-29

### Content

- Added three new public pages to give the site the depth and originality
  Google's AdSense review expects: `/how-to-use` (a step-by-step conversion
  guide), `/examples` (common Markdown inputs paired with their exact,
  freshly-generated HTML output), and `/faq` (an expanded question set
  covering privacy, browser requirements, downloads, copying, upload
  limits, and unsupported syntax, with `FAQPage` structured data).
- Expanded `/about` with a "Who built it, and why" section and a "Who this
  is for" use-case list (bloggers/writers, students/researchers,
  developers, small businesses), and added a matching compact use-case
  list to the homepage's syntax section.
- Linked the new pages from the header nav, footer nav, and relevant
  homepage sections on every public page, and normalized every page's
  footer to list the full site instead of each page selectively omitting
  itself and its siblings.

### Technical

- Routed `/how-to-use`, `/examples`, and `/faq` in `api/index.py`'s page
  table and added them to `sitemap.xml`; `robots.txt` already allowed all
  non-`/api/` paths so no change was needed there.
- Added route tests confirming the three new pages serve 200 with expected
  `<h1>` content, carry the AdSense verification tag, and appear in
  `sitemap.xml`.

### Testing

- Re-verified the three adversarial-input performance tests named in the
  AdSense follow-up work — they already pass (no ReDoS regression since
  the v2.1.0 emphasis-span fix). Full suite: 127 passed.

## [2.1.2] - 2026-07-22

### Fixed

- Prevented a slow complete-document download request from saving stale HTML
  after the Markdown, title, theme, output type, or table-of-contents setting
  changes. In-flight downloads are now aborted and sequence-checked before a
  file can be created.

### Testing

- Added regression coverage for stale-download invalidation and the public
  API's conversion-timeout `503` response.

### Documentation

- Corrected the release handoff so its current version and operational notes
  match the shipped product.

## [2.1.1] - 2026-07-22

### AdSense

- Added the `google-adsense-account` verification meta tag to every public
  page (converter, About, Privacy, Terms, Support), alongside the existing
  verification script and `ads.txt` entry — the three methods Google's
  AdSense dashboard offers for site verification.

## [2.1.0] - 2026-07-22

### Brand

- Applied the CSolutions identity mark to the site header and favicon.

### AdSense

- Added the verified AdSense publisher script and authorized `ads.txt` entry.
- Added nonce-based strict CSP handling for AdSense without removing framing,
  base URI, object, or upgrade protections (further narrowed below).
- Updated the privacy disclosure while keeping visible ad placements disabled
  until site approval.

### Security

- Fixed a ReDoS (catastrophic backtracking) vulnerability in the bold/italic
  regexes: a 750,000-character adversarial payload of unmatched `*`/`_`
  characters previously took 10+ seconds to parse; emphasis spans are now
  bounded to 200 characters, bringing worst-case parse time down to a few
  seconds.
- Added an 8-second wall-clock timeout around every `/api/convert` request
  as a backstop against any pathological input the length/span bounds don't
  anticipate, returning a `503` instead of tying up the invocation.
- Narrowed the AdSense CSP from a blanket `https:`/`http:` allowance to the
  specific Google ad-serving hosts required, and removed `'unsafe-eval'`.
- Protected inline code spans from later bold/italic reprocessing, so
  `` `**not bold**` `` renders literally instead of as `<strong>`.

### Fixed

- Copy HTML and Download no longer hand out stale output: the editor
  invalidates the previous conversion immediately on input instead of only
  after the 450ms debounce settles.
- Hard line breaks (two trailing spaces) are preserved again; a prior
  paragraph-joining bug silently dropped them.
- Duplicate headings now get unique `id` attributes (`overview`,
  `overview-2`, ...) instead of colliding on the same anchor.
- Table of contents nesting now produces valid, well-formed `<ul>`/`<li>`
  markup, including when heading levels jump (e.g. h1 directly to h3).
- HTML fragment mode now includes the table of contents when
  `includeToc` is enabled, instead of silently ignoring the setting.
- Preview/HTML source tabs now support full keyboard operation: arrow keys,
  Home/End, and roving tabindex, with `role="tabpanel"` wired to the
  correct tab via `aria-labelledby`.
- Reduced redundant per-keystroke work: character/word/line stats and
  local-draft saves now run once per debounce cycle instead of twice
  (once eagerly, once after the delay), cutting main-thread work on large
  documents.

### Testing

- Added 24 regression tests covering duplicate heading IDs, inline code
  protection, hard line breaks, nested/fragment TOC output, and adversarial
  parser timing (both Python-level and through the live HTTP API).
- Added `.flake8` so `flake8`'s line-length and ignore settings actually
  match `pyproject.toml`'s `[tool.flake8]` table (vanilla flake8 does not
  read `pyproject.toml`), and brought the whole codebase to a clean
  `black --check` / `flake8` pass.

### Documentation

- Updated README, ADSENSE.md, and HANDOFF.md to reflect that the custom
  domain is live (not a future step), the actual parser limits, and the
  current AdSense/CMP status.

## [2.0.0] - 2026-07-21

### Security

- Escaped document titles, attribute values, and code-language classes.
- Rejected unsafe link and image URL schemes.
- Added external-link rel protection and a sandboxed preview.
- Added request, Markdown, title, content-type, JSON, and field validation.
- Confined static file resolution and removed internal exception details.
- Added CSP, framing, MIME, referrer, permissions, and no-store headers.

### Product

- Rebuilt the web converter with preview and HTML-source tabs.
- Added fragment and complete-document modes, reliable copy/download behavior,
  upload limits, counters, samples, status states, and local draft recovery.
- Prevented stale conversion races with abortable sequenced requests.
- Added responsive and accessible layouts for mobile through desktop.

### Discovery and operations

- Added accurate metadata, canonical URLs, Open Graph data, crawler files,
  application/FAQ structured data, visible educational content, and real 404s.
- Added About, Privacy, Terms, and Support pages.
- Added disabled ad-placement infrastructure and AdSense activation guidance.
- Removed Flask requirements and tracked generated artifacts.
- Aligned package, documentation, and release version at 2.0.0.

[2.2.0]: https://github.com/Crespo1301/MarkdownToHTML/releases/tag/v2.2.0
[2.1.2]: https://github.com/Crespo1301/MarkdownToHTML/releases/tag/v2.1.2
[2.1.1]: https://github.com/Crespo1301/MarkdownToHTML/releases/tag/v2.1.1
[2.1.0]: https://github.com/Crespo1301/MarkdownToHTML/releases/tag/v2.1.0
[2.0.0]: https://github.com/Crespo1301/MarkdownToHTML/releases/tag/v2.0.0
