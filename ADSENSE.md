# Future AdSense activation

Advertising is intentionally disabled. No publisher ID, `ads.txt`, Google ad
script, analytics script, or consent platform is present.

When a real AdSense account is approved:

1. Review the live content, navigation, Privacy page, Terms page, and Support
   route before submitting the site.
2. Configure Google's Privacy & Messaging flow or another Google-certified CMP
   where consent is required.
3. Add the real publisher ID through a Vercel environment variable. Never commit
   it as a guessed or placeholder value.
4. Add Google's exact script only after consent requirements are implemented.
5. Enable the reserved `data-ad-slot="content-after-tool"` region after the
   converter workflow. Keep ads away from editor and Copy, Download, Upload,
   Clear, theme, and output controls.
6. Publish `ads.txt` only with the exact line supplied by the approved account.
7. Update the Privacy page with the active providers, cookies, purposes,
   retention, and opt-out or consent controls before loading ads.
8. Test mobile layout, keyboard order, CLS, and accidental-click risk.

The reserved region is hidden and non-interactive until activation.
