import assert from "node:assert/strict";
import test from "node:test";

import { isMarkdownDocumentInfo, makePreviewTitle } from "../src/extensionSupport";

test("recognizes Markdown documents by language id or file extension", () => {
  assert.equal(isMarkdownDocumentInfo({ languageId: "markdown", fileName: "README.txt" }), true);
  assert.equal(isMarkdownDocumentInfo({ languageId: "plaintext", fileName: "README.md" }), true);
  assert.equal(isMarkdownDocumentInfo({ languageId: "plaintext", fileName: "README.markdown" }), true);
  assert.equal(isMarkdownDocumentInfo({ languageId: "plaintext", fileName: "theme.css" }), false);
});

test("creates a predictable preview title", () => {
  assert.equal(makePreviewTitle("C:\\Users\\cloudy\\README.md"), "README.md Preview");
  assert.equal(makePreviewTitle("/tmp/notes/design.markdown"), "design.markdown Preview");
});
