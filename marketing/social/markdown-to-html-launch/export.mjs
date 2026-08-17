import { createRequire } from "node:module";
import { mkdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
const playwrightRoot =
  process.env.PLAYWRIGHT_ROOT ||
  "/home/cresp3/.visual-runner/node_modules/playwright";
const { chromium } = require(playwrightRoot);

const here = dirname(fileURLToPath(import.meta.url));
const source = pathToFileURL(resolve(here, "promo.html")).href;
const exportDir = resolve(here, "exports");
await mkdir(exportDir, { recursive: true });

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ deviceScaleFactor: 1 });

for (const slide of ["1", "2", "3", "4", "5"]) {
  await page.setViewportSize({ width: 1080, height: 1350 });
  await page.goto(`${source}?slide=${slide}`, { waitUntil: "networkidle" });
  await page.screenshot({
    path: resolve(exportDir, `carousel-${slide}.png`),
    clip: { x: 0, y: 0, width: 1080, height: 1350 },
  });
}

for (const slide of ["1", "2", "3", "4", "5"]) {
  await page.setViewportSize({ width: 1080, height: 1920 });
  await page.goto(`${source}?slide=${slide}&format=tiktok`, {
    waitUntil: "networkidle",
  });
  await page.screenshot({
    path: resolve(exportDir, `tiktok-${slide}.png`),
    clip: { x: 0, y: 0, width: 1080, height: 1920 },
  });
}

for (const slide of ["1", "2", "3", "4", "5"]) {
  await page.setViewportSize({ width: 1080, height: 1920 });
  await page.goto(`${source}?slide=${slide}&format=tiktok&safe=1`, {
    waitUntil: "networkidle",
  });
  await page.screenshot({
    path: resolve(exportDir, `tiktok-safe-check-${slide}.png`),
    clip: { x: 0, y: 0, width: 1080, height: 1920 },
  });
}

await page.setViewportSize({ width: 1080, height: 1920 });
await page.goto(`${source}?slide=story`, { waitUntil: "networkidle" });
await page.screenshot({
  path: resolve(exportDir, "story-cover.png"),
  clip: { x: 0, y: 0, width: 1080, height: 1920 },
});

await browser.close();
console.log(`Exported campaign to ${exportDir}`);
