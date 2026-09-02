# Release handoff

## Release

- Current: `v2.2.0` — added `/how-to-use`, `/examples`, and `/faq` content
  pages plus an expanded `/about`, targeting the AdSense "site needs more
  original, helpful content" gap, on top of the existing functionality,
  security, accessibility, and AdSense-verification work.
- Canonical origin in code: `https://mdtohtmlconverter.com` (live)
- Existing Vercel project: `markdown-to-html`
- Existing production alias: `https://markdown-to-html-iota.vercel.app`

## Post-tag local maintenance (2026-09-02)

- The runtime package and CLI now report `2.2.0`, matching `pyproject.toml`,
  README, CHANGELOG, and the documented release. Commit `2d2e91e` added the
  alignment and regression tests; no new release tag was created.
- `MASTER_RULES_AI.md` is now tracked as the repo-specific writing and workflow
  policy. The 2026-09-01 rule commits are documentation-only.

- Aligned `templates/privacy.html` with `ADSENSE.md`: verification code remains
  present for review, visible ads remain disabled, and no CMP or analytics is
  claimed until actually configured.
- The launch campaign remains local and untracked under `marketing/`; review
  and commit it separately before distribution.

## AdSense status (2026-07-29)

- Google Search Console domain property is verified (confirmed by Carlos).
  `sitemap.xml` — now including `/how-to-use`, `/examples`, and `/faq` — has
  been submitted; resubmit it in Search Console if it wasn't already
  resubmitted after this release.
- AdSense has **not** approved the site yet. v2.2.0's new content pages are
  the response to the prior generic "meet program policies" rejection and
  are intended to support a resubmission — they are not a guarantee of
  approval. Do not claim or imply AdSense approval anywhere in the codebase
  or public copy until Google's dashboard actually shows it.
- Visible ad placements remain disabled (`.ad-region[hidden]` in
  `templates/index.html`) until approval. See `ADSENSE.md` for the exact
  post-approval activation steps — do not skip ahead of them.

## v2.2.0 decisions

- AdSense had not approved the site under the generic "Meet AdSense program
  policies" reason. Rather than guess further, treated it as a content-depth
  problem: added three new standalone pages instead of stuffing more content
  onto the homepage, so the converter stays the focus and the new material
  reads as genuinely useful rather than padding.
- Generated every "Markdown in → HTML out" example shown on `/how-to-use`
  and `/examples` by actually running the parser/converter locally, rather
  than hand-writing plausible-looking output — this matters because the
  parser has real quirks (e.g. nested lists don't nest inside the parent
  `<li>`) that a fabricated example would have hidden or gotten wrong. The
  nested-list case was deliberately left out of the public examples in favor
  of a flat list, since showing it without explanation would read as a bug
  report rather than documentation.
- Chose `/how-to-use` over the suggested `/guides/markdown-to-html` — a flat
  path fits the router's existing flat page-table pattern and there's no
  second guide planned that would justify a `/guides/` segment.
- Normalized every page's footer nav to list the whole site (previously each
  page selectively omitted itself and one or two siblings, which was an
  inconsistent, error-prone pattern to maintain as pages were added).
- Did not touch `static/js/app.js`, the parser/converter, CSP, or ads.txt —
  out of scope for a content pass, and the brief was explicit about
  preserving sanitizer/parser behavior and security posture.
- Re-ran the three named adversarial-input performance tests; all pass
  under the existing `MAX_EMPHASIS_SPAN` bound from v2.1.0 with no
  regression, so no parser change was needed this round.

## Launch campaign assets

- Local source: `marketing/social/markdown-to-html-launch/`
- Deliverables: Instagram carousel, Story/Reel cover, TikTok carousel,
  TikTok contact sheet, TikTok safe-zone proof sheet, editable HTML/CSS source,
  and campaign ZIP.
- The campaign is CSolutions-branded, uses solid colors only, and is built
  around real production screenshots from `v2.1.2`.
- Review `marketing/social/markdown-to-html-launch/HANDOFF.md` before posting
  or changing copy. Critical text in TikTok exports is kept inside the
  documented safe frame; proof exports are for QA only and should not be posted.

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
   `https://mdtohtmlconverter.com/sitemap.xml`. Done — domain property
   verified (confirmed 2026-07-29). Resubmit `sitemap.xml` after v2.2.0 so
   Search Console picks up `/how-to-use`, `/examples`, and `/faq`.
10. Update the Portfolio project URL only after the custom domain serves the
    production deployment successfully. Done — see
    `/home/cresp3/Portfolio/src/data/projects.ts`.
11. Apply for AdSense only after the domain, content, legal pages, and support
    navigation are live. Follow `ADSENSE.md` after approval. **Still open** —
    site is submitted for review; not yet approved. v2.2.0 added the content
    depth intended to support a resubmission (see "AdSense status" above).
    Visible ad units remain disabled until Google's approval.
