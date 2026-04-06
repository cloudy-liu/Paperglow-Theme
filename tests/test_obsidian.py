from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
THEME_PATH = ROOT_DIR / "theme.css"
MANIFEST_PATH = ROOT_DIR / "manifest.json"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_block(css: str, selector: str) -> str:
    marker = f"{selector} {{"
    start = css.find(marker)
    if start == -1:
        return ""

    index = start + len(marker)
    depth = 1
    while index < len(css) and depth > 0:
        if css[index] == "{":
            depth += 1
        elif css[index] == "}":
            depth -= 1
        index += 1

    return css[start:index]


def extract_rule_with_flexible_selector(css: str, selector_pattern: str) -> str:
    match = re.search(rf"({selector_pattern})\s*\{{(?P<body>.*?)\}}", css, re.S)
    if not match:
        return ""
    return match.group("body")


def collect_missing_items() -> list[str]:
    missing: list[str] = []

    readme_path = ROOT_DIR / "README.md"

    if not THEME_PATH.exists():
        missing.append(f"Theme file missing: {THEME_PATH}")
        return missing

    if not MANIFEST_PATH.exists():
        missing.append(f"Manifest file missing: {MANIFEST_PATH}")
        return missing

    if not readme_path.exists():
        missing.append(f"README missing: {readme_path}")
        return missing

    css = read_text(THEME_PATH)
    readme = read_text(readme_path)
    manifest = json.loads(read_text(MANIFEST_PATH))

    if manifest.get("name") != "Paperglow":
        missing.append('Manifest "name" should be "Paperglow"')
    if not manifest.get("version"):
        missing.append('Manifest "version" should not be empty')
    if not manifest.get("author"):
        missing.append('Manifest "author" should not be empty')

    required_css_markers = [
        ".theme-light",
        ".theme-dark",
        "--background-primary",
        "--text-normal",
        "--color-accent",
        "--font-text-theme",
        '"Montserrat"',
        ".markdown-rendered blockquote",
        ".markdown-rendered pre",
        ".callout",
        "#bc6a3a",
        "#d59567",
        "border-radius: 16px",
    ]
    for marker in required_css_markers:
        if marker not in css:
            missing.append(f"Theme CSS marker missing: {marker}")

    required_readme_markers = [
        "python install.py obsidian --vault",
        ".obsidian/themes/Paperglow/",
        "theme.css",
        "manifest.json",
        "Apache License 2.0",
    ]
    for marker in required_readme_markers:
        if marker not in readme:
            missing.append(f"README marker missing: {marker}")

    return missing


def main() -> int:
    missing = collect_missing_items()
    if missing:
        for item in missing:
            print(item, file=sys.stderr)
        return 1

    print("Obsidian Paperglow theme checks passed.")
    return 0


class ObsidianThemeTest(unittest.TestCase):
    def test_obsidian_theme_assets(self) -> None:
        missing = collect_missing_items()
        self.assertEqual(missing, [], "\n".join(missing))

    def test_live_preview_base_typography_excludes_special_blocks(self) -> None:
        css = read_text(THEME_PATH)

        live_preview_body = extract_rule_with_flexible_selector(
            css,
            r"\.markdown-source-view\.mod-cm6\.is-live-preview \.cm-line:not\(\.HyperMD-codeblock\):"
            r"not\(\.HyperMD-header\):not\(\.HyperMD-quote\):not\(\.HyperMD-hr\):not\(\.HyperMD-table-row\)",
        )

        self.assertIn("color: var(--text-normal);", live_preview_body)
        self.assertIn("line-height: 1.5;", live_preview_body)

    def test_h5_h6_headings_are_not_uppercased_in_obsidian(self) -> None:
        css = read_text(THEME_PATH)

        heading_body = extract_rule_with_flexible_selector(
            css,
            r"\.markdown-rendered h5,\s*"
            r"\.markdown-rendered h6,\s*"
            r"\.markdown-source-view\.mod-cm6\.is-live-preview \.HyperMD-header-5,\s*"
            r"\.markdown-source-view\.mod-cm6\.is-live-preview \.HyperMD-header-6",
        )

        self.assertIn("color: var(--text-normal);", heading_body)
        self.assertIn("letter-spacing: normal;", heading_body)
        self.assertIn("text-transform: none;", heading_body)

    def test_reading_view_lists_keep_obsidian_defaults_with_accent_markers(self) -> None:
        css = read_text(THEME_PATH)
        body = extract_block(css, "body")
        marker_tokens = extract_rule_with_flexible_selector(
            css,
            r"\.markdown-rendered,\s*"
            r"\.markdown-preview-view,\s*"
            r"\.markdown-source-view\.mod-cm6",
        )
        reading_ordered_marker = extract_rule_with_flexible_selector(
            css,
            r"\.markdown-rendered ol > li::marker,\s*"
            r"\.markdown-preview-view ol > li::marker",
        )
        reading_bullet_base = extract_block(css, ".markdown-rendered .list-bullet::after")
        reading_bullet_solid = extract_rule_with_flexible_selector(
            css,
            r"\.markdown-rendered ul > li > \.list-bullet::after,\s*"
            r"\.markdown-rendered ul ul ul ul > li > \.list-bullet::after,\s*"
            r"\.markdown-rendered ul ul ul ul ul ul ul > li > \.list-bullet::after",
        )
        reading_bullet_hollow = extract_rule_with_flexible_selector(
            css,
            r"\.markdown-rendered ul ul > li > \.list-bullet::after,\s*"
            r"\.markdown-rendered ul ul ul ul ul > li > \.list-bullet::after,\s*"
            r"\.markdown-rendered ul ul ul ul ul ul ul ul > li > \.list-bullet::after",
        )
        reading_bullet_square = extract_rule_with_flexible_selector(
            css,
            r"\.markdown-rendered ul ul ul > li > \.list-bullet::after,\s*"
            r"\.markdown-rendered ul ul ul ul ul ul > li > \.list-bullet::after,\s*"
            r"\.markdown-rendered ul ul ul ul ul ul ul ul ul > li > \.list-bullet::after",
        )

        self.assertIn("--pg-list-ordered-marker-size: 0.92em;", body)
        self.assertIn("--pg-list-bullet-size-round: 0.3em;", body)
        self.assertIn("--pg-list-bullet-size-square: 0.24em;", body)
        self.assertIn("--list-marker-color: rgba(var(--accent-rgb), 0.78);", marker_tokens)
        self.assertIn("--list-marker-color-hover: rgba(var(--accent-rgb), 0.9);", marker_tokens)
        self.assertIn("--list-marker-color-collapsed: rgba(var(--accent-rgb), 0.58);", marker_tokens)
        self.assertIn("color: var(--list-marker-color);", reading_ordered_marker)
        self.assertIn("font-size: var(--pg-list-ordered-marker-size);", reading_ordered_marker)
        self.assertIn("font-weight: 600;", reading_ordered_marker)
        self.assertIn("box-shadow: none;", reading_bullet_base)
        self.assertIn("background-color: var(--list-marker-color);", reading_bullet_solid)
        self.assertIn("border-radius: 999px;", reading_bullet_solid)
        self.assertIn("height: var(--pg-list-bullet-size-round);", reading_bullet_solid)
        self.assertIn("background-color: transparent;", reading_bullet_hollow)
        self.assertIn("border: 1.2px solid var(--list-marker-color);", reading_bullet_hollow)
        self.assertIn("border-radius: 999px;", reading_bullet_hollow)
        self.assertIn("background-color: var(--list-marker-color);", reading_bullet_square)
        self.assertIn("border-radius: 1px;", reading_bullet_square)
        self.assertIn("height: var(--pg-list-bullet-size-square);", reading_bullet_square)

        self.assertNotIn("counter(pg-ol-item", css)
        self.assertNotIn("--pg-list-root-indent", body)
        self.assertNotIn("--pg-list-bullet-gutter", body)

    def test_live_preview_lists_only_tint_markers_and_reduce_ordered_size(self) -> None:
        css = read_text(THEME_PATH)
        ordered_body = extract_rule_with_flexible_selector(
            css,
            r"\.markdown-source-view\.mod-cm6\.is-live-preview "
            r"\.HyperMD-list-line \.cm-formatting-list-ol,\s*"
            r"\.markdown-source-view\.mod-cm6\.is-live-preview "
            r"\.HyperMD-list-line \.list-number",
        )
        live_bullet_base = extract_block(
            css,
            ".markdown-source-view.mod-cm6.is-live-preview .HyperMD-list-line .list-bullet::after",
        )
        live_bullet_solid = extract_rule_with_flexible_selector(
            css,
            r"\.markdown-source-view\.mod-cm6\.is-live-preview "
            r"\.HyperMD-list-line-1 \.list-bullet::after,\s*"
            r"\.markdown-source-view\.mod-cm6\.is-live-preview "
            r"\.HyperMD-list-line-4 \.list-bullet::after,\s*"
            r"\.markdown-source-view\.mod-cm6\.is-live-preview "
            r"\.HyperMD-list-line-7 \.list-bullet::after",
        )
        live_bullet_hollow = extract_rule_with_flexible_selector(
            css,
            r"\.markdown-source-view\.mod-cm6\.is-live-preview "
            r"\.HyperMD-list-line-2 \.list-bullet::after,\s*"
            r"\.markdown-source-view\.mod-cm6\.is-live-preview "
            r"\.HyperMD-list-line-5 \.list-bullet::after,\s*"
            r"\.markdown-source-view\.mod-cm6\.is-live-preview "
            r"\.HyperMD-list-line-8 \.list-bullet::after",
        )
        live_bullet_square = extract_rule_with_flexible_selector(
            css,
            r"\.markdown-source-view\.mod-cm6\.is-live-preview "
            r"\.HyperMD-list-line-3 \.list-bullet::after,\s*"
            r"\.markdown-source-view\.mod-cm6\.is-live-preview "
            r"\.HyperMD-list-line-6 \.list-bullet::after,\s*"
            r"\.markdown-source-view\.mod-cm6\.is-live-preview "
            r"\.HyperMD-list-line-9 \.list-bullet::after",
        )

        self.assertIn("font-size: var(--pg-list-ordered-marker-size);", ordered_body)
        self.assertIn("color: var(--list-marker-color);", ordered_body)
        self.assertIn("font-weight: 600;", ordered_body)
        self.assertIn("box-shadow: none;", live_bullet_base)
        self.assertIn("background-color: var(--list-marker-color);", live_bullet_solid)
        self.assertIn("border-radius: 999px;", live_bullet_solid)
        self.assertIn("background-color: transparent;", live_bullet_hollow)
        self.assertIn("border: 1.2px solid var(--list-marker-color);", live_bullet_hollow)
        self.assertIn("border-radius: 999px;", live_bullet_hollow)
        self.assertIn("background-color: var(--list-marker-color);", live_bullet_square)
        self.assertIn("border-radius: 1px;", live_bullet_square)

        self.assertNotIn("min-width: var(--pg-list-ordered-marker-width);", ordered_body)
        self.assertNotIn("padding-right: var(--pg-list-ordered-marker-gap);", ordered_body)
        self.assertNotIn("font-weight: var(--pg-list-ordered-marker-weight);", ordered_body)


if __name__ == "__main__":
    unittest.main()
