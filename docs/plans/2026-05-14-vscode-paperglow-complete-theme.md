# VS Code Paperglow Complete Theme Implementation Plan

Date: 2026-05-14

## Goal

Upgrade the VS Code package from a custom Markdown-preview extension into a
complete Paperglow theme extension. Users should select **Paperglow Light** or
**Paperglow Dark** as their VS Code color theme, then keep using VS Code's
built-in Markdown source/preview workflow.

## Final Architecture

- `vscode/package.json` contributes two VS Code color themes:
  `Paperglow Light` and `Paperglow Dark`.
- `vscode/package.json` contributes `markdown.previewStyles` so VS Code's
  native Markdown preview loads Paperglow reading CSS.
- Theme JSON files own workbench colors and syntax colors.
- `vscode/media/paperglow-markdown-preview.css` owns native Markdown preview
  typography and content styling, scoped to the Paperglow theme IDs.
- No custom Markdown preview command, editor-title action, Webview runtime, or
  `Preview | Markdown` toggle remains in the extension.

## Completed Tasks

### 1. Theme Contribution Contract

- Renamed the VS Code package to `paperglow-theme`.
- Updated Marketplace metadata to position the package as a complete theme.
- Added `Paperglow Light` and `Paperglow Dark` theme contributions.
- Added static tests that parse `package.json` and the contributed theme files.

### 2. Workbench and Syntax Baseline

- Added light and dark workbench colors for visible VS Code surfaces: activity
  bar, side bar, tree/list states, editor, tabs, panels, terminal, status bar,
  quick input, notifications, focus rings, git decorations, and badges.
- Added TextMate and semantic token baselines for common source and Markdown
  scopes.
- Tuned dark foreground brightness against Atom One Dark's quieter reading
  level.
- Tuned light list selection, hover states, and status bar item states after
  manual review.

### 3. Native Markdown Preview Styling

- Replaced the old custom preview stylesheet with native Markdown preview CSS.
- Scoped preview styling to:
  - `body[data-vscode-theme-id="Paperglow Light"]`
  - `body[data-vscode-theme-id="Paperglow Dark"]`
- Aligned typography, headings, paragraphs, blockquotes, links, inline code,
  code blocks, tables, images, and responsive spacing with the Paperglow reading
  style.
- Removed custom Webview chrome, background cards, table hover artifacts, and
  linked-code underline edges.

### 4. Extension Icon

- Added a packaged PNG extension icon and kept the SVG source beside it.
- Limited the mark to the paper/book shape instead of the old banner treatment.
- Enlarged the visible PNG alpha bounds so the icon aligns with other VS Code
  extension-list icons.

### 5. Docs and Packaging

- Updated `vscode/README.md` to document theme selection and native Markdown
  preview usage.
- Simplified packaging: no runtime bundle, no Webview dependencies, and no
  shipped test or source files.
- Regenerated `vscode/paperglow-theme.vsix`.

## Verification Commands

Run from the repository root unless noted:

```powershell
Push-Location vscode
npm test
npm run package:vsix
Pop-Location
python -m unittest discover -s tests -p "test_*.py"
```

## GitHub Tracking

- Parent PRD: #20
- Visual QA: #24
- Native preview refactor and manual polish trail: #25
- Implementation PR: #19

