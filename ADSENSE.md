# Future AdSense activation

The site is connected to AdSense publisher `pub-9248605150391626` for review.
The account verification script and authorized `ads.txt` entry are live in the
codebase. Visible ad units remain disabled until Google approves the site.

Loading the verification script before approval is intentional — Google
requires it on the page to review the site. The CSP that permits it
(`ADSENSE_CSP` in `api/index.py`) is scoped to the specific Google
ad-serving hosts documented below (`pagead2.googlesyndication.com`,
`adservice.google.com`, `googletagservices.com`,
`partner.googleadservices.com`, `tpc.googlesyndication.com`,
`googleads.g.doubleclick.net`, and `*.google.com`) rather than a blanket
`https:`, and omits `'unsafe-eval'` and `http:`. If live ad creatives later
require directives this list doesn't cover, widen it deliberately and
re-verify with `git diff` — don't fall back to a wildcard policy.

Monetization strategy: AdSense display ads on organic/search traffic. This
is not a paid Google Ads acquisition campaign — no ad spend is budgeted to
drive traffic to the site.

No consent management platform (CMP) is configured yet. Do not describe
this site as having consent controls in any public copy until step 2 below
is actually done and verified in the browser.

After Google approves the site:

1. Review the live content, navigation, Privacy page, Terms page, and Support
   route before submitting the site.
2. Configure Google's Privacy & Messaging flow or another Google-certified CMP
   where consent is required.
3. Keep the publisher ID and account code exact. The customer ID is internal and
   must not be added to public code.
4. Create responsive ad units in AdSense and copy their exact slot IDs.
5. Enable the reserved `data-ad-slot="content-after-tool"` region after the
   converter workflow. Keep ads away from editor and Copy, Download, Upload,
   Clear, theme, and output controls.
6. Confirm AdSense reports the existing `ads.txt` entry as Authorized.
7. Update the Privacy page with the active providers, cookies, purposes,
   retention, and opt-out or consent controls before loading ads.
8. Test mobile layout, keyboard order, CLS, and accidental-click risk.

The reserved region is hidden and non-interactive until activation.
