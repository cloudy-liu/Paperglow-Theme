import assert from "node:assert/strict";
import test from "node:test";

import { getMarkdownFeatureSupport } from "../src/markdownFeatureScope";

test("documents the v1 advanced Markdown support boundary", () => {
  const support = getMarkdownFeatureSupport();

  assert.equal(support.table, "supported");
  assert.equal(support.taskList, "supported");
  assert.equal(support.mermaid, "deferred");
  assert.equal(support.math, "deferred");
  assert.equal(support.obsidianCallout, "deferred");
  assert.equal(support.customContainer, "deferred");
});
