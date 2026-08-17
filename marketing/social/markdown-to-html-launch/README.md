# MarkdownToHTML Launch Campaign

Editable, screenshot-led promotional media for the public launch of
[mdtohtmlconverter.com](https://mdtohtmlconverter.com).

This campaign is designed for publication from the CSolutions brand account. It
uses solid colors only, with no gradients or glass effects.

## Deliverables

- Five `1080x1350` Instagram carousel slides
- One `1080x1920` Story/Reel cover
- Five `1080x1920` TikTok carousel slides
- One TikTok contact sheet for quick review
- One TikTok safe-zone proof sheet for checking interface overlap
- Exact HTML/CSS source for continued editing
- Campaign copy, alt text, and motion notes in `HANDOFF.md`

## Export

```bash
cd /home/cresp3/MarkdownToHTML/marketing/social/markdown-to-html-launch
node export.mjs
bash contact-sheet.sh
```

The script uses the shared Playwright installation under
`/home/cresp3/.visual-runner` and writes PNG files to `exports/`.

TikTok exports are named `tiktok-1.png` through `tiktok-5.png`. They retain
the approved campaign system while using the full vertical canvas and keeping
key copy clear of TikTok's interface zones.

The TikTok proof exports are named `tiktok-safe-check-1.png` through
`tiktok-safe-check-5.png`, with a review sheet at
`exports/tiktok-safe-zone-check.png`. These proof files include a red content
frame only for QA. Do not post the proof images.

## Source Assets

The campaign uses real production captures from version `2.1.2`. It does not
contain generated interfaces, fake analytics, or invented product claims.
