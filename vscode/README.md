# Paperglow Markdown Preview

Paperglow Markdown Preview adds a single-tab Markdown preview workflow to VS Code.
It is designed for users who want a Cursor-like `Preview | Markdown` switch
without replacing VS Code's native Markdown editor.

## Usage

1. Open a Markdown file.
2. Run **Paperglow: Open Paperglow Preview** from the Command Palette, or click
   the Paperglow preview action in the editor title area.
3. Read the document in the Paperglow preview.
4. Click **Markdown** in the preview header to return to the source editor.

The preview opens in the current editor group. It does not default to a split
view.

## Product Boundary

This extension does not provide Typora-style WYSIWYG editing. Markdown source is
still edited by VS Code's native editor. Paperglow owns only the preview Webview
and its compact document header.

## v1 Markdown Scope

| Feature | Status |
| --- | --- |
| Headings, paragraphs, blockquotes, lists | Supported |
| Task lists | Supported |
| Tables | Supported |
| Code blocks and inline code | Supported |
| Links and images | Supported |
| Frontmatter | Deferred |
| Mermaid | Deferred |
| Math | Deferred |
| Obsidian callouts | Deferred |
| Custom containers | Deferred |

## Preview Assets

Screenshots should be added before Marketplace publication:

- Light Paperglow preview
- Dark Paperglow preview
- Narrow editor width with a long file name
