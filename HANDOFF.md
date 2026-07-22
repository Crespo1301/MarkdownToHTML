# Release handoff

## Release

- Target: `v2.0.0`
- Canonical origin in code: `https://mdtohtmlconverter.com`
- Existing Vercel project: `markdown-to-html`
- Existing production alias: `https://markdown-to-html-iota.vercel.app`

## Decisions

- Preserve the zero-runtime-dependency parser and CLI rather than introducing a
  large parsing dependency in this release.
- Escape raw HTML and allowlist URL schemes at the parser seam so CLI, library,
  and web callers share the same protection.
- Keep the tool first; educational, FAQ, privacy, and discovery content follows.
- Use schema.org microdata so structured data exactly matches visible content
  without weakening script CSP for inline JSON-LD.
- Treat Copy HTML as the selected output mode. Download always produces a
  complete styled document.

## Domain launch checklist

Do not copy generic DNS values. Add both domains in Vercel first, then use the
exact records Vercel displays for this project.

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
   `https://mdtohtmlconverter.com/sitemap.xml`.
10. Update the Portfolio project URL only after the custom domain serves the
    production deployment successfully.
11. Apply for AdSense only after the domain, content, legal pages, and support
    navigation are live. Follow `ADSENSE.md` after approval.
