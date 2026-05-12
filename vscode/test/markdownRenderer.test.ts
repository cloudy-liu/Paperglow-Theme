import assert from "node:assert/strict";
import test from "node:test";

import { createMarkdownRenderer } from "../src/markdownRenderer";

test("renders common Markdown blocks and maps links and images", () => {
  const renderer = createMarkdownRenderer({
    resolveImageSrc: (src) => `safe-image:${src}`,
    resolveLinkHref: (href) => `safe-link:${href}`,
  });

  const html = renderer.render(`# Title

> Quote

- [x] Done
- Item

| A | B |
| - | - |
| 1 | 2 |

\`\`\`ts
const value = 1;
\`\`\`

![Alt](./docs/light.png)

[External](https://example.com)

---`);

  assert.match(html, /<h1>Title<\/h1>/);
  assert.match(html, /<blockquote>/);
  assert.match(html, /type="checkbox"/);
  assert.match(html, /<table>/);
  assert.match(html, /class="language-ts"/);
  assert.match(html, /src="safe-image:\.\/docs\/light\.png"/);
  assert.match(html, /href="safe-link:https:\/\/example\.com"/);
  assert.match(html, /data-href="https:\/\/example\.com"/);
  assert.match(html, /<hr\s*\/?>/);
});

test("escapes raw HTML by default", () => {
  const renderer = createMarkdownRenderer();

  const html = renderer.render("<script>alert(1)</script>");

  assert.doesNotMatch(html, /<script>alert/);
});

test("renders safe inline HTML used by project README files", () => {
  const renderer = createMarkdownRenderer({
    resolveImageSrc: (src: string) => `safe-image:${src}`,
  });

  const html = renderer.render(`<p align="center">
  <img src="docs/logo.svg" alt="Paperglow logo" width="680" />
</p>

<table>
  <tr>
    <td><img src="docs/typora/light-1.png" alt="Typora preview 1" width="480" /></td>
    <td>Preview</td>
  </tr>
</table>`);

  assert.match(html, /<p align="center">/);
  assert.match(html, /<img src="safe-image:docs\/logo\.svg" alt="Paperglow logo" width="680" \/>/);
  assert.match(html, /<table>/);
  assert.match(html, /<td><img src="safe-image:docs\/typora\/light-1\.png" alt="Typora preview 1" width="480" \/><\/td>/);
});

test("strips unsafe HTML while preserving readable text", () => {
  const renderer = createMarkdownRenderer();

  const html = renderer.render(
    '<p onclick="alert(1)">Keep me</p><img src="javascript:alert(1)" onerror="alert(1)"><script>alert(1)</script>',
  );

  assert.match(html, /<p>Keep me<\/p>/);
  assert.doesNotMatch(html, /onclick/);
  assert.doesNotMatch(html, /onerror/);
  assert.doesNotMatch(html, /javascript:/);
  assert.doesNotMatch(html, /<script>/);
});
