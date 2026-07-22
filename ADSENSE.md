# Future AdSense activation

The site is connected to AdSense publisher `pub-9248605150391626` for review.
The account verification script and authorized `ads.txt` entry are live in the
codebase. Visible ad units remain disabled until Google approves the site.

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
