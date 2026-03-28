<p align="center">
  <img src="docs/logo.svg" alt="Paperglow logo" width="560" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Apps-Obsidian%20%2B%20Typora-bc6a3a?style=flat-square" alt="Apps: Obsidian and Typora" />
  <img src="https://img.shields.io/badge/Version-0.2.0-d59567?style=flat-square" alt="Version: 0.2.0" />
  <img src="https://img.shields.io/badge/License-Apache%202.0-6f5b4b?style=flat-square" alt="License: Apache 2.0" />
</p>

[简体中文](README.md) | English

# Paperglow Theme

Paperglow is a warm paper-inspired theme for Typora and Obsidian. It replaces flat white canvases with sunlit paper tones, quiet burnt-clay accents, and a softer dark palette that feels closer to a late-night study than a terminal.

## Highlights

- Warm paper light mode and deep-ink dark mode
- Rounded reading-card surfaces for both writing and preview areas
- Unified Montserrat / Noto Sans SC / JetBrains Mono typography
- Soft quote blocks, 16px code blocks, clay-toned links, and consistent callouts

## Preview

### Obsidian

<p align="center">
  <img src="docs/obsidian/light.png" alt="Obsidian light mode preview" width="900" />
</p>

<p align="center">
  <img src="docs/obsidian/dark.png" alt="Obsidian dark mode preview" width="900" />
</p>

### Typora

<table>
  <tr>
    <td><img src="docs/typora/light-1.png" alt="Typora preview 1" width="480"/></td>
    <td><img src="docs/typora/light-2.png" alt="Typora preview 2" width="480"/></td>
  </tr>
  <tr>
    <td><img src="docs/typora/light-3.png" alt="Typora preview 3" width="480"/></td>
    <td><img src="docs/typora/light-4.png" alt="Typora preview 4" width="480"/></td>
  </tr>
  <tr>
    <td><img src="docs/typora/dark-1.png" alt="Typora preview 5" width="480"/></td>
    <td><img src="docs/typora/dark-2.png" alt="Typora preview 6" width="480"/></td>
  </tr>
</table>

## Supported Apps

| App | Theme | Status | Path |
|-----|-------|--------|------|
| Obsidian | Paperglow | ✅ Maintained | [`theme.css`](theme.css) + [`manifest.json`](manifest.json) |
| Typora | Paperglow | ✅ Maintained | [`typora/`](typora/) |

## Install

The repository ships with a lightweight installer script at [`install.py`](install.py), so you can install the theme directly without an extra packaging step.

### Obsidian

```bash
python install.py obsidian
```

The script can discover local vaults automatically. To target a single vault:

```bash
python install.py obsidian --vault "/path/to/your/vault"
```

### Typora

```bash
python install.py typora
```

Install to a custom theme directory:

```bash
python install.py typora --target-dir "C:\path\to\Typora\themes"
```

## Manual Install

### Obsidian

Copy [`theme.css`](theme.css) and [`manifest.json`](manifest.json) into `<vault>/.obsidian/themes/Paperglow/`, then select **Paperglow** in **Settings → Appearance → Themes**.

### Typora

Copy [`paperglow.css`](typora/paperglow.css) and [`paperglow-dark.css`](typora/paperglow-dark.css) into your Typora themes directory. `paperglow-dark.css` uses `@import` to load `./paperglow.css`, so both files must exist together.

| Platform | Path |
|----------|------|
| Windows | `%APPDATA%\Typora\themes\` |
| macOS | `~/Library/Application Support/abnerworks.Typora/themes/` |
| Linux | `~/.config/Typora/themes/` |

## Notes

### Typora Windows Unibody Title Bar

Paperglow styles the editor, sidebar, search panel, and part of Typora's HTML UI, but the default Windows title bar is still a native system control. If you want the top area to feel visually consistent with Paperglow, switch Typora to **Settings / Preferences → Appearance → Window Style → Unibody**, then restart Typora.

### Obsidian Highlights

- Shared Montserrat / Noto Sans SC / JetBrains Mono font system
- Warm paper light palette paired with a quieter deep-ink dark palette
- Card-like reading surfaces in both editing and reading views
- 16px code blocks, warm-gray blockquotes, clay-toned links, and aligned callouts

## License

Apache License 2.0
