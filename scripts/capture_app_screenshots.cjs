const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright-core");

const root = path.resolve(__dirname, "..");
const outDir = path.join(root, "demo_recordings", "scratch-wallet-app-captures", "screenshots");
const chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const appUrl = process.env.SCRATCH_WALLET_APP_URL || "http://127.0.0.1:8505";

fs.mkdirSync(outDir, { recursive: true });

async function clickVisible(page, label) {
  const streamlitLabel = page.locator("label").filter({ hasText: label });
  if (await streamlitLabel.count()) {
    await streamlitLabel.first().click({ force: true });
    await page.waitForTimeout(1800);
    return true;
  }
  const button = page.getByRole("button", { name: label });
  if (await button.count()) {
    await button.first().click();
    await page.waitForTimeout(1800);
    return true;
  }
  const exact = page.getByText(label, { exact: true });
  if (await exact.count()) {
    await exact.first().click({ force: true });
    await page.waitForTimeout(1800);
    return true;
  }
  const fuzzy = page.getByText(label);
  if (await fuzzy.count()) {
    await fuzzy.first().click({ force: true });
    await page.waitForTimeout(1800);
    return true;
  }
  return false;
}

async function shot(page, name) {
  await page.screenshot({
    path: path.join(outDir, `${name}.png`),
    fullPage: false,
  });
}

async function clickSidebar(page, y) {
  await page.mouse.click(84, y);
  await page.waitForTimeout(2200);
}

async function selectNav(page, label) {
  const clicked = await page.evaluate((target) => {
    const options = Array.from(document.querySelectorAll('[data-testid="stRadioOption"]'));
    const option = options.find((el) => (el.innerText || el.textContent || "").trim() === target);
    if (!option) return false;
    option.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true, view: window }));
    return true;
  }, label);
  if (!clicked) {
    throw new Error(`Navigation option not found: ${label}`);
  }
  await page.waitForTimeout(2600);
}

(async () => {
  const browser = await chromium.launch({
    executablePath: chromePath,
    headless: true,
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  await page.goto(appUrl, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForTimeout(5000);

  await shot(page, "01_demo_intro");
  await clickVisible(page, "🎫 Scratch Today") || await clickVisible(page, "Scratch Today");
  await page.waitForTimeout(3000);
  await shot(page, "02_demo_scratch_today");
  await clickVisible(page, "Mock Anchor");
  await page.waitForTimeout(1800);
  await shot(page, "03_demo_mock_anchor");

  const pages = [
    ["04_scratch_card", "Scratch Card"],
    ["05_control_room", "Control Room"],
    ["06_claim_shield", "Claim Shield"],
    ["07_anchor_deploy", "Anchor / Deploy"],
    ["08_video_submit", "Video / Submit"],
    ["09_submission", "Submission"],
    ["10_form_fields", "Form Fields"],
  ];
  for (const [name, label] of pages) {
    await page.goto(`${appUrl}?page=${encodeURIComponent(label)}`, { waitUntil: "domcontentloaded", timeout: 60000 });
    await page.waitForTimeout(4000);
    await shot(page, name);
  }

  await browser.close();
  console.log(outDir);
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
