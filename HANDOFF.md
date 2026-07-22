# Release handoff

## Release

- Current: `v2.1.2` — functionality, security, accessibility, content,
  AdSense site verification, and stale-output protection on top of the live
  production converter.
- Canonical origin in code: `https://mdtohtmlconverter.com` (live)
- Existing Vercel project: `markdown-to-html`
- Existing production alias: `https://markdown-to-html-iota.vercel.app`

## v2.1.2 decisions

- An in-flight complete-document download is now aborted when the editor
  changes, and its request sequence is checked before a file can be saved.
  This extends the existing stale-preview protections to the download path.
- Added regression coverage for download invalidation and the public API's
  timeout-to-`503` response.

## v2.1.1 decisions

- Added Google's `google-adsense-account` verification meta tag to every
  public page, alongside the existing verification script and authorized
  `ads.txt` entry.
- Kept visible ad placements disabled while Google reviews the site. Approval
  and responsive ad-slot activation remain separate operator actions described
  in `ADSENSE.md`.

## v2.1.0 decisions

- Bounded the emphasis regexes (`MarkdownParser.MAX_EMPHASIS_SPAN = 200`)
  rather than switching to a different parsing library, to fix the ReDoS
  while keeping the zero-runtime-dependency parser. Tradeoff: emphasized
  spans longer than 200 characters render as literal `**`/`*` text.
  Documented in README under "Parser limits and abuse protection".
  The senior review pass suggested raising this to ~2000, citing a
  measured 0.24s parse time at that cap; re-measured directly in a fresh
  process against the same 750,000-character adversarial input and got
  17.8s at cap 2000, 9.7s at cap 1000, and 4.9s at cap 500 — all confirming
  the expected roughly-linear-in-cap cost and contradicting the cited
  figure. Kept the cap at 200 (~2.1s worst case, verified reproducible)
  rather than reintroducing a multi-second parse on adversarial input.
- Added an 8-second wall-clock guard (`signal.alarm`) around conversion as
  defense-in-depth, not as the primary fix — it degrades gracefully (no-op)
  under the threaded test server, where `signal.alarm` isn't usable.
- Chose to make fragment mode support the table of contents (rather than
  disabling the "Include table of contents" checkbox in fragment mode),
  since a working fragment TOC is more useful for CMS embedding than an
  extra disabled-state UI branch.
- Narrowed the AdSense CSP to specific Google hosts using a third-party
  reference guide (no official Google page was reachable to verify against
  during this pass — see ADSENSE.md). Revisit against Google's current
  guidance before widening it for live ad creatives.
- Deferred the "Editor / Preview / Source mode switch" mobile redesign
  suggested for a heavier design pass — the current stacked layout is
  functional and accessible at 360-390px, but a single-pane mode switch
  would meaningfully speed up the mobile workflow. Tracked as fast-follow.

## v2.0.0 decisions

- Preserve the zero-runtime-dependency parser and CLI rather than introducing a
  large parsing dependency in this release.
- Escape raw HTML and allowlist URL schemes at the parser seam so CLI, library,
  and web callers share the same protection.
- Keep the tool first; educational, FAQ, privacy, and discovery content follows.
- Use schema.org microdata so structured data exactly matches visible content
  without weakening script CSP for inline JSON-LD.
- Treat Copy HTML as the selected output mode. Download always produces a
  complete styled document.

## Domain launch (complete)

`mdtohtmlconverter.com` is live in production: HTTP redirects to HTTPS, `www`
redirects once to the apex, and canonical tags, Open Graph URLs,
`robots.txt`, and `sitemap.xml` all use `https://mdtohtmlconverter.com`. The
steps below are kept for reference (e.g. re-pointing DNS after a registrar
change), not as pending work.

1. Buy `mdtohtmlconverter.com` in Porkbun.
2. In Vercel, open project `markdown-to-html`, then Settings, Domains.
3. Add `mdtohtmlconverter.com`, then add `www.mdtohtmlconverter.com`.
4. Set the apex domain as production and configure `www` to redirect to the
   apex domain.
5. In Porkbun DNS, add the exact A, CNAME, or TXT verification records Vercel
   shows. Remove only conflicting records for those same hostnames.
6. Wait for both domains to show Valid Configuration and for Vercel to issue
   SSL certificates.
7. Verify HTTP redirects to HTTPS and `www` redirects once to the apex.
8. Verify canonical tags, Open Graph URLs, `robots.txt`, and `sitemap.xml` use
   `https://mdtohtmlconverter.com`.
9. Add a Domain property in Google Search Console. Copy Google's exact DNS TXT
   verification value into Porkbun, verify ownership, then submit
   `https://mdtohtmlconverter.com/sitemap.xml`. **Still open** — confirm this
   has actually been done; it is not verifiable from the codebase.
10. Update the Portfolio project URL only after the custom domain serves the
    production deployment successfully. Done — see
    `/home/cresp3/Portfolio/src/data/projects.ts`.
11. Apply for AdSense only after the domain, content, legal pages, and support
    navigation are live. Follow `ADSENSE.md` after approval. **Still open** —
    site is submitted for review; visible ad units remain disabled pending
    Google's approval.
