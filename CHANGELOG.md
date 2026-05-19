# Changelog

All notable changes to Paperglow are listed here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.1] - 2026-05-20

### Fixed
- Keep the Typora outline/sidebar usable with long nested documents.
- Improve Mermaid readability in Typora dark mode, including node shapes and sequence diagram actor labels.

### Changed
- Improve VS Code / Cursor VSIX installation guidance in both Chinese and English READMEs, including command-line setup, UI installation, and theme activation steps.
- Document what to do when the `code` or `cursor` command is not available in the terminal.

## [0.3.0] - 2026-05-16

### Added
- VS Code / Cursor native theme with full **Paperglow Light** and **Paperglow Dark** workbench and syntax palettes.
- Built-in VS Code Markdown preview styled to match the active Paperglow theme via `markdown.previewStyles`.
- Release workflow now builds and ships a `paperglow-vscode.vsix` artifact alongside the Obsidian and Typora bundles.

### Changed
- README documents the VS Code installation flow and updates the supported-apps table and project structure.

## [0.2.3] - 2026-05-05

- Maintenance release for Obsidian and Typora packaging.
