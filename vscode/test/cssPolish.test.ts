import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

const cssPath = path.resolve(__dirname, "../../media/paperglow-markdown-preview.css");

test("scopes native Markdown preview styling to Paperglow themes", () => {
  const css = readFileSync(cssPath, "utf8");

  assert.match(css, /body\[data-vscode-theme-id="Paperglow Light"\]/);
  assert.match(css, /body\[data-vscode-theme-id="Paperglow Dark"\]/);
  assert.doesNotMatch(css, /body\.vscode-light\s*\{/);
  assert.doesNotMatch(css, /body\.vscode-dark\s*\{/);
});

test("aligns native Markdown preview typography with Typora Paperglow", () => {
  const css = readFileSync(cssPath, "utf8");

  assert.match(css, /--pg-font-body:\s*"Montserrat"/);
  assert.match(css, /"Noto Sans SC"/);
  assert.match(css, /"PingFang SC"/);
  assert.match(css, /font-size:\s*1\.0625rem;/);
  assert.match(css, /line-height:\s*1\.5;/);
  assert.match(css, /max-width:\s*1100px;/);
});

test("keeps the native Markdown preview unframed inside the VS Code shell", () => {
  const css = readFileSync(cssPath, "utf8");

  assert.match(css, /\.markdown-body\s*\{[\s\S]*background:\s*transparent;/);
  assert.match(css, /\.markdown-body\s*\{[\s\S]*border:\s*0;/);
  assert.match(css, /\.markdown-body\s*\{[\s\S]*border-radius:\s*0;/);
  assert.match(css, /\.markdown-body\s*\{[\s\S]*box-shadow:\s*none;/);
  assert.doesNotMatch(css, /--pg-paper-bg/);
  assert.doesNotMatch(css, /--pg-paper-shadow/);
});

test("styles native Markdown reading elements without custom Webview chrome", () => {
  const css = readFileSync(cssPath, "utf8");

  assert.match(css, /blockquote\s*\{[\s\S]*border-left:\s*3px solid var\(--pg-quote-border\);/);
  assert.match(css, /pre\s*\{[\s\S]*border-radius:\s*16px;/);
  assert.match(css, /table\s*\{[\s\S]*border-collapse:\s*collapse;/);
  assert.match(css, /a\s*\{[\s\S]*border-bottom:\s*1\.5px solid var\(--pg-link-border\);/);
  assert.doesNotMatch(css, /\.pg-doc-header/);
  assert.doesNotMatch(css, /\.pg-mode-switch/);
  assert.doesNotMatch(css, /\.pg-markdown-source/);
});

test("keeps inline code pills consistent and removes linked-code edge artifacts", () => {
  const css = readFileSync(cssPath, "utf8");

  assert.match(css, /code\s*\{[\s\S]*background-color:\s*var\(--pg-inline-code-bg\);/);
  assert.match(css, /code\s*\{[\s\S]*border:\s*1px solid var\(--pg-inline-code-border\);/);
  assert.match(css, /code\s*\{[\s\S]*border-radius:\s*999px;/);
  assert.match(css, /code\s*\{[\s\S]*padding:\s*2px 10px;/);
  assert.match(css, /code::before,[\s\S]*code::after\s*\{[\s\S]*content:\s*none;/);
  assert.match(css, /a:has\(>\s*code:only-child\)\s*\{[\s\S]*border-bottom:\s*0;/);
  assert.match(css, /table code\s*\{[\s\S]*background-color:\s*var\(--pg-inline-code-bg\);/);
  assert.match(css, /table code\s*\{[\s\S]*border:\s*1px solid var\(--pg-inline-code-border\);/);
  assert.match(css, /th,[\s\S]*td\s*\{[\s\S]*line-height:\s*1\.7;/);
  assert.match(css, /thead tr,[\s\S]*tbody tr,[\s\S]*tr:nth-child\(2n\)\s*\{[\s\S]*background:\s*transparent;/);
  assert.match(css, /table tr::before\s*\{[\s\S]*content:\s*none;/);
  assert.doesNotMatch(css, /--pg-table-inline-code/);
  assert.doesNotMatch(css, /tr:hover/);
  assert.doesNotMatch(css, /--pg-table-hover/);
});

test("softens dark Markdown preview text for the VS Code shell", () => {
  const css = readFileSync(cssPath, "utf8");
  const darkBlock = css.match(/body\[data-vscode-theme-id="Paperglow Dark"\]\s*\{([\s\S]*?)\n\}/)?.[1] ?? "";

  assert.match(darkBlock, /--pg-text:\s*#bdb1a4;/i);
  assert.match(darkBlock, /--pg-heading:\s*#d8cdc0;/i);
  assert.match(darkBlock, /--pg-muted:\s*#9e9489;/i);
  assert.match(darkBlock, /--pg-quote-text:\s*#b6aa9e;/i);
});

test("keeps the native preview free of old custom-preview color drift", () => {
  const css = readFileSync(cssPath, "utf8");

  assert.doesNotMatch(css, /#4aa3ff/i);
  assert.doesNotMatch(css, /#24272d/i);
  assert.doesNotMatch(css, /rgba\(188,\s*106,\s*58,\s*0\.28\)/i);
});
