# Changelog

All notable changes follow semantic versioning.

## [Unreleased]

### AdSense

- Added the verified AdSense publisher script and authorized `ads.txt` entry.
- Added nonce-based strict CSP handling for AdSense without removing framing,
  base URI, object, or upgrade protections.
- Updated the privacy disclosure while keeping visible ad placements disabled
  until site approval.

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

[2.0.0]: https://github.com/Crespo1301/MarkdownToHTML/releases/tag/v2.0.0
