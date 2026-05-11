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
  assert.match(html, /<hr>/);
});

test("escapes raw HTML by default", () => {
  const renderer = createMarkdownRenderer();

  const html = renderer.render("<script>alert(1)</script>");

  assert.match(html, /&lt;script&gt;alert\(1\)&lt;\/script&gt;/);
  assert.doesNotMatch(html, /<script>alert/);
});
