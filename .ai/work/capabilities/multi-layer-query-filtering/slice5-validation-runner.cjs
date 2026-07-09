const fs = require("fs");
const path = require("path");
const zlib = require("zlib");
const { chromium } = require("playwright");

const baseUrl = process.env.SLICE5_BASE_URL || "http://127.0.0.1:8771/";
const outDir = path.resolve(__dirname, "slice5-validation-2026-07-09");

fs.mkdirSync(outDir, { recursive: true });

const result = {
  baseUrl,
  checks: [],
  screenshots: [],
  console: []
};

function record(name, pass, details = {}) {
  result.checks.push({ name, pass: Boolean(pass), details });
  if (!pass) {
    const error = new Error(`${name} failed`);
    error.details = details;
    throw error;
  }
}

function crc32(buffer) {
  let crc = -1;
  for (const byte of buffer) {
    crc ^= byte;
    for (let bit = 0; bit < 8; bit += 1) {
      crc = (crc >>> 1) ^ (0xedb88320 & -(crc & 1));
    }
  }
  return (crc ^ -1) >>> 0;
}

function pngChunk(type, data) {
  const typeBuffer = Buffer.from(type, "ascii");
  const length = Buffer.alloc(4);
  length.writeUInt32BE(data.length, 0);
  const crc = Buffer.alloc(4);
  crc.writeUInt32BE(crc32(Buffer.concat([typeBuffer, data])), 0);
  return Buffer.concat([length, typeBuffer, data, crc]);
}

function transparentPngTile(size = 256) {
  const signature = Buffer.from("89504e470d0a1a0a", "hex");
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(size, 0);
  ihdr.writeUInt32BE(size, 4);
  ihdr[8] = 8;
  ihdr[9] = 6;
  const stride = 1 + size * 4;
  const raw = Buffer.alloc(stride * size);
  for (let row = 0; row < size; row += 1) raw[row * stride] = 0;
  return Buffer.concat([
    signature,
    pngChunk("IHDR", ihdr),
    pngChunk("IDAT", zlib.deflateSync(raw)),
    pngChunk("IEND", Buffer.alloc(0))
  ]);
}

async function screenshot(page, name) {
  const file = path.join(outDir, `${name}.png`);
  await page.screenshot({ path: file, fullPage: false });
  result.screenshots.push(path.relative(process.cwd(), file));
}

async function waitForApp(page) {
  await page.waitForSelector("#layerSelectorSearch:not([disabled])", { timeout: 15000 });
  await page.waitForFunction(() => !document.querySelector("#layerSelectorStatus")?.textContent.trim(), null, { timeout: 15000 });
}

async function openLayer(page, query, layerId, label) {
  await page.fill("#layerSelectorSearch", query);
  const option = page.locator(`[data-layer-select="${layerId.replace(/"/g, '\\"')}"]`);
  await option.waitFor({ state: "visible", timeout: 15000 });
  await option.click();
  await page.waitForFunction(
    title => [...document.querySelectorAll("button.raw-source-tab")].some(tab => tab.getAttribute("title") === title),
    label,
    { timeout: 15000 }
  );
}

async function switchLayer(page, label) {
  const tab = page.locator(`button.raw-source-tab[title="${label.replace(/"/g, '\\"')}"]`);
  await tab.waitFor({ state: "visible", timeout: 15000 });
  await tab.click();
  await page.waitForFunction(
    title => document.querySelector("button.raw-source-tab.active")?.getAttribute("title") === title,
    label,
    { timeout: 15000 }
  );
}

async function openFilter(page) {
  const isOpen = await page.evaluate(() => !document.querySelector("#layerFilterPanel")?.hidden);
  if (isOpen) return;
  await page.click("button.raw-source-tab.active [data-layer-filter]");
  await page.waitForFunction(() => !document.querySelector("#layerFilterPanel")?.hidden, null, { timeout: 15000 });
}

async function setFilter(page, field, value) {
  await openFilter(page);
  if (await page.locator("[data-filter-field]").count() === 0) {
    await page.click("[data-filter-add]");
    await page.waitForSelector("[data-filter-field]", { timeout: 15000 });
  }
  await page.locator("[data-filter-field]").first().selectOption(field);
  await page.locator("[data-filter-value]").first().fill(value);
}

async function applyFilter(page) {
  await page.click("[data-filter-apply]");
  await page.waitForTimeout(250);
}

async function summary(page) {
  return page.evaluate(() => {
    const active = document.querySelector("button.raw-source-tab.active");
    return {
      title: active?.getAttribute("title") || "",
      countText: active?.querySelector("strong")?.textContent.trim() || "",
      rows: document.querySelectorAll("#evidenceRows tr").length,
      empty: document.querySelector("#evidenceRows .empty-cell")?.textContent.trim() || "",
      filterOpen: !document.querySelector("#layerFilterPanel")?.hidden,
      filterError: document.querySelector(".filter-error")?.textContent.trim() || "",
      mapMarkers: document.querySelectorAll(".map-marker").length,
      timelineItems: document.querySelectorAll(".timeline-item").length,
      activeHidden: active?.classList.contains("hidden-source") || false,
      overlayMinimized: document.querySelector("#rawEventsOverlay")?.classList.contains("minimized") || false,
      tabs: [...document.querySelectorAll("button.raw-source-tab")].map(tab => tab.getAttribute("title"))
    };
  });
}

async function main() {
  const browser = await chromium.launch({ channel: "msedge", headless: true });
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  const transparentPng = transparentPngTile();
  await page.route("**/*", route => {
    if (!route.request().url().includes("tile.openstreetmap.org/")) {
      route.continue();
      return;
    }
    route.fulfill({
      status: 200,
      contentType: "image/png",
      body: transparentPng
    });
  });
  page.on("console", message => {
    if (["warning", "warn", "error"].includes(message.type())) {
      result.console.push({ type: message.type(), text: message.text() });
    }
  });
  page.on("pageerror", error => result.console.push({ type: "pageerror", text: error.message }));

  await page.goto(baseUrl, { waitUntil: "load" });
  await waitForApp(page);

  await openLayer(page, "טלגרם", "events:טלגרם", "טלגרם");
  await openLayer(page, "חדשות", "events:חדשות מקומיות", "חדשות מקומיות");
  await openLayer(page, "ישויות", "entity-metadata:all", "שכבת ישויות");
  await openLayer(page, "מיקומים", "location-metadata:all", "שכבת מיקומים");
  let state = await summary(page);
  record("required layer families opened", ["טלגרם", "חדשות מקומיות", "שכבת ישויות", "שכבת מיקומים"].every(label => state.tabs.includes(label)), state);

  await switchLayer(page, "טלגרם");
  await openFilter(page);
  await screenshot(page, "01-mobile-all-layers-filter-open");

  await setFilter(page, "source_type", "");
  await applyFilter(page);
  state = await summary(page);
  record("empty value blocking", state.filterError.includes("יש למלא"), state);

  await setFilter(page, "source_type", "טלגרם");
  await applyFilter(page);
  state = await summary(page);
  record("event-source Hebrew contains filter", state.countText === "1,280/1,280" && state.rows > 0 && state.mapMarkers > 0, state);
  await screenshot(page, "02-mobile-event-hebrew-filter-nonzero");

  await switchLayer(page, "חדשות מקומיות");
  await setFilter(page, "source_reliability_label", "unverified");
  await applyFilter(page);
  const localNews = await summary(page);
  record("second event-source English contains filter", /^\d+\/1,307$/.test(localNews.countText) && !localNews.countText.startsWith("0/"), localNews);

  await switchLayer(page, "טלגרם");
  state = await summary(page);
  record("independent event-source filter preserved", state.countText === "1,280/1,280", state);

  await switchLayer(page, "שכבת ישויות");
  await setFilter(page, "canonical_name", "KFOR");
  await applyFilter(page);
  state = await summary(page);
  record("Entities layer English contains filter", state.countText === "1/16" && state.rows === 1, state);

  await switchLayer(page, "שכבת מיקומים");
  await setFilter(page, "municipality", "צפון");
  await applyFilter(page);
  state = await summary(page);
  record("Locations layer Hebrew contains filter", /^\d+\/155$/.test(state.countText) && !state.countText.startsWith("0/"), state);
  await screenshot(page, "03-mobile-entities-locations-filtered");

  await setFilter(page, "municipality", "definitely-no-match-value");
  await applyFilter(page);
  state = await summary(page);
  record("no-results behavior", state.countText === "0/155" && state.empty.includes("ריקה"), state);
  await screenshot(page, "04-mobile-zero-result-state");

  await page.click('[data-view="timeline"]');
  await page.waitForFunction(() => document.querySelector('[data-view="timeline"]')?.classList.contains("active"), null, { timeout: 15000 });
  state = await summary(page);
  record("timeline renders event layers", state.timelineItems > 0, state);

  await switchLayer(page, "טלגרם");
  await page.click("button.raw-source-tab.active [data-layer-visibility]");
  await page.waitForFunction(() => document.querySelector("button.raw-source-tab.active")?.classList.contains("hidden-source"), null, { timeout: 15000 });
  state = await summary(page);
  record("visibility hides active layer rows", state.activeHidden && state.empty.includes("מוסתרת"), state);
  await page.click("button.raw-source-tab.active [data-layer-visibility]");
  await page.waitForFunction(() => !document.querySelector("button.raw-source-tab.active")?.classList.contains("hidden-source"), null, { timeout: 15000 });

  await page.click("#rawEventsMinimize");
  await page.waitForFunction(() => document.querySelector("#rawEventsOverlay")?.classList.contains("minimized"), null, { timeout: 15000 });
  await page.click("#rawEventsMinimize");
  await page.waitForFunction(() => !document.querySelector("#rawEventsOverlay")?.classList.contains("minimized"), null, { timeout: 15000 });
  state = await summary(page);
  record("minimize and restore", !state.overlayMinimized, state);

  const beforeHeight = await page.evaluate(() => getComputedStyle(document.querySelector("#rawEventsOverlay")).getPropertyValue("--raw-overlay-height"));
  const handle = page.locator("#rawEventsResizeHandle");
  const box = await handle.boundingBox();
  record("resize handle present", Boolean(box), box || {});
  await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
  await page.mouse.down();
  await page.mouse.move(box.x + box.width / 2, Math.max(80, box.y - 80));
  await page.mouse.up();
  const afterHeight = await page.evaluate(() => getComputedStyle(document.querySelector("#rawEventsOverlay")).getPropertyValue("--raw-overlay-height"));
  record("resize drag checked", Boolean(afterHeight), { beforeHeight, afterHeight });

  await page.locator('button.raw-source-tab[title="חדשות מקומיות"] [data-layer-close]').click();
  await page.waitForFunction(() => ![...document.querySelectorAll("button.raw-source-tab")].some(tab => tab.getAttribute("title") === "חדשות מקומיות"), null, { timeout: 15000 });
  state = await summary(page);
  record("close removes selected layer only", !state.tabs.includes("חדשות מקומיות") && state.tabs.includes("טלגרם") && state.tabs.includes("שכבת ישויות") && state.tabs.includes("שכבת מיקומים"), state);

  await page.setViewportSize({ width: 768, height: 1024 });
  await page.reload({ waitUntil: "load" });
  await waitForApp(page);
  await openLayer(page, "טלגרם", "events:טלגרם", "טלגרם");
  await setFilter(page, "source_type", "טלגרם");
  await applyFilter(page);
  state = await summary(page);
  record("tablet viewport smoke", state.countText === "1,280/1,280" && state.filterOpen, state);
  await screenshot(page, "05-tablet-filtered-state");

  await page.setViewportSize({ width: 1366, height: 900 });
  await page.reload({ waitUntil: "load" });
  await waitForApp(page);
  await openLayer(page, "ישויות", "entity-metadata:all", "שכבת ישויות");
  await setFilter(page, "canonical_name", "KFOR");
  await applyFilter(page);
  state = await summary(page);
  record("desktop viewport smoke", state.countText === "1/16" && state.filterOpen, state);
  await screenshot(page, "06-desktop-filtered-state");
  record("console clean of app warnings and errors", result.console.length === 0, { console: result.console });

  await browser.close();

  const report = {
    ...result,
    passed: result.checks.every(check => check.pass),
    warningCount: result.console.length
  };
  fs.writeFileSync(path.join(outDir, "validation-result.json"), JSON.stringify(report, null, 2), "utf8");
  console.log(JSON.stringify(report, null, 2));
}

main().catch(error => {
  result.error = { message: error.message, details: error.details || null, stack: error.stack };
  fs.writeFileSync(path.join(outDir, "validation-result.json"), JSON.stringify(result, null, 2), "utf8");
  console.error(JSON.stringify(result, null, 2));
  process.exit(1);
});
