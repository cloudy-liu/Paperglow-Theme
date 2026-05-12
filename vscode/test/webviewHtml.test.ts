import assert from "node:assert/strict";
import test from "node:test";

import { buildWebviewHtml } from "../src/webviewHtml";

test("builds a preview document with file identity and compact mode switch", () => {
  const html = buildWebviewHtml({
    fileName: "README<script>.md",
    bodyHtml: "<h1>Paperglow Theme</h1>",
    markdownText: "# Paperglow Theme",
    styleUri: "vscode-resource://style.css",
    cspSource: "vscode-resource:",
    nonce: "abc123",
  });

  assert.match(html, /README&lt;script&gt;\.md/);
  assert.match(html, /class="pg-doc-header"/);
  assert.match(html, /data-mode-target="preview"[^>]*aria-pressed="true"[^>]*>Preview<\/button>/);
  assert.match(html, /data-mode-target="markdown"[^>]*aria-pressed="false"[^>]*>Markdown<\/button>/);
  assert.match(html, /<h1>Paperglow Theme<\/h1>/);
  assert.match(html, /<pre class="pg-markdown-source"[^>]*><code># Paperglow Theme<\/code><\/pre>/);
  assert.match(html, /Content-Security-Policy/);
  assert.match(html, /script-src 'nonce-abc123'/);
  assert.match(html, /img-src vscode-resource: https: data:/);
});

test("switches Markdown mode inside the Paperglow webview instead of opening the source editor", () => {
  const html = buildWebviewHtml({
    fileName: "README.md",
    bodyHtml: "<p>Preview</p>",
    markdownText: "# Preview\n\n<script>alert(1)</script>",
    styleUri: "style.css",
    cspSource: "vscode-resource:",
    nonce: "nonce",
  });

  assert.doesNotMatch(html, /openSource/);
  assert.doesNotMatch(html, /postMessage\(\{\s*type:\s*"openSource"/);
  assert.match(html, /data-command="setMode"/);
  assert.match(html, /data-mode-panel="preview"/);
  assert.match(html, /data-mode-panel="markdown" hidden/);
  assert.match(html, /&lt;script&gt;alert\(1\)&lt;\/script&gt;/);
  assert.match(html, /vscode\.setState\(\{ mode \}\)/);
});

test("does not escape already-rendered trusted Markdown body HTML", () => {
  const html = buildWebviewHtml({
    fileName: "README.md",
    bodyHtml: "<blockquote><p>Quote</p></blockquote>",
    markdownText: "> Quote",
    styleUri: "style.css",
    cspSource: "vscode-resource:",
    nonce: "nonce",
  });

  assert.match(html, /<blockquote><p>Quote<\/p><\/blockquote>/);
});
