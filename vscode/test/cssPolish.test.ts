import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

const cssPath = path.resolve(__dirname, "../../media/paperglow-preview.css");

test("keeps the preview header compact", () => {
  const css = readFileSync(cssPath, "utf8");

  assert.match(css, /--pg-header-height:\s*40px;/);
  assert.match(css, /\.pg-file-identity\s*\{[\s\S]*font-size:\s*13px;/);
  assert.match(css, /\.pg-mode-switch\s*\{[\s\S]*height:\s*26px;/);
  assert.match(css, /\.pg-mode\s*\{[\s\S]*font:\s*500 12px\/1/);
});

test("uses an unframed reading surface instead of a floating card", () => {
  const css = readFileSync(cssPath, "utf8");

  assert.match(css, /\.pg-reading-card\s*\{[\s\S]*background:\s*transparent;/);
  assert.match(css, /\.pg-reading-card\s*\{[\s\S]*border:\s*0;/);
  assert.match(css, /\.pg-reading-card\s*\{[\s\S]*box-shadow:\s*none;/);
  assert.match(css, /\.pg-reading-card\s*\{[\s\S]*border-radius:\s*0;/);
});
