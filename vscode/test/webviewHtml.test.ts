import assert from "node:assert/strict";
import test from "node:test";

import { buildWebviewHtml } from "../src/webviewHtml";

test("builds a preview document with file identity and compact mode switch", () => {
  const html = buildWebviewHtml({
    fileName: "README<script>.md",
    bodyHtml: "<h1>Paperglow Theme</h1>",
    styleUri: "vscode-resource://style.css",
    cspSource: "vscode-resource:",
    nonce: "abc123",
  });

  assert.match(html, /README&lt;script&gt;\.md/);
  assert.match(html, /class="pg-doc-header"/);
  assert.match(html, /class="pg-mode is-active"[^>]*>Preview<\/span>/);
  assert.match(html, /data-command="openSource"[^>]*>Markdown<\/button>/);
  assert.match(html, /<h1>Paperglow Theme<\/h1>/);
  assert.match(html, /Content-Security-Policy/);
  assert.match(html, /script-src 'nonce-abc123'/);
  assert.match(html, /img-src vscode-resource: https: data:/);
});

test("does not escape already-rendered trusted Markdown body HTML", () => {
  const html = buildWebviewHtml({
    fileName: "README.md",
    bodyHtml: "<blockquote><p>Quote</p></blockquote>",
    styleUri: "style.css",
    cspSource: "vscode-resource:",
    nonce: "nonce",
  });

  assert.match(html, /<blockquote><p>Quote<\/p><\/blockquote>/);
});
