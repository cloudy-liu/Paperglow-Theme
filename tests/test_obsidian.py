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


def extract_rules_with_flexible_selector(css: str, selector_pattern: str) -> list[str]:
    return [
        match.group("body")
        for match in re.finditer(rf"({selector_pattern})\s*\{{(?P<body>.*?)\}}", css, re.S)
    ]


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

    def test_reading_mode_code_blocks_show_language_labels(self) -> None:
        css = read_text(THEME_PATH)

        self.assertIn('.markdown-rendered pre[class*="language-"]::before', css)
        self.assertIn(
            '.markdown-rendered pre:has(> code[class*="language-"])::before',
            css,
        )
        self.assertIn("--pg-code-language-block-padding: 16px 20px;", css)
        self.assertIn("content: var(--pg-code-language-label, none);", css)
        self.assertIn("opacity: 0;", css)
        self.assertIn("transition: opacity 0.15s ease;", css)
        self.assertIn('.markdown-rendered pre[class*="language-"]:hover::before', css)
        self.assertIn(
            '.markdown-rendered pre:has(> code[class*="language-"]):focus-within::before',
            css,
        )
        self.assertIn(
            '.markdown-rendered pre:has(> code[class~="language-shell"])',
            css,
        )
        self.assertNotIn('--pg-code-language-block-padding: 42px', css)
        self.assertIn('--pg-code-language-label: "Shell";', css)
        self.assertIn('--pg-code-language-label: "JSON";', css)
        self.assertIn('--pg-code-language-label: "CSS";', css)

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

    def test_hovered_links_do_not_add_browser_underlines(self) -> None:
        css = read_text(THEME_PATH)
        body = extract_block(css, "body")
        hover_body = extract_rule_with_flexible_selector(
            css,
            r"\.markdown-rendered a:hover,\s*"
            r"\.cm-link:hover,\s*"
            r"\.external-link:hover,\s*"
            r"\.internal-link:hover",
        )

        self.assertIn("--link-decoration-hover: none;", body)
        self.assertIn("--link-external-decoration-hover: none;", body)
        self.assertIn("text-decoration: none;", hover_body)

    def test_live_preview_blockquotes_match_reading_mode(self) -> None:
        css = read_text(THEME_PATH)

        live_quote_rules = extract_rules_with_flexible_selector(
            css,
            r"\.markdown-source-view\.mod-cm6\.is-live-preview \.HyperMD-quote",
        )
        self.assertGreaterEqual(len(live_quote_rules), 2)
        live_quote_shared = next(
            body for body in live_quote_rules if "background: var(--blockquote-background-color);" in body
        )
        live_quote_layout = next(body for body in live_quote_rules if "padding:" in body)
        reading_quote_body = extract_rule_with_flexible_selector(
            css,
            r"\.markdown-rendered blockquote p,\s*"
            r"\.markdown-rendered blockquote li",
        )
        live_quote_border = extract_rule_with_flexible_selector(
            css,
            r"\.markdown-source-view\.mod-cm6\.is-live-preview \.HyperMD-quote:before",
        )
        nested_quote_border = extract_rule_with_flexible_selector(
            css,
            r"\.markdown-source-view\.mod-cm6 \.cm-blockquote-border:before",
        )
        blank_live_quote = extract_rule_with_flexible_selector(
            css,
            r"\.markdown-source-view\.mod-cm6\.is-live-preview "
            r"\.HyperMD-quote:not\(:has\(\.cm-quote\)\)",
        )
        live_quote_start = extract_rule_with_flexible_selector(
            css,
            r"\.markdown-source-view\.mod-cm6\.is-live-preview "
            r"\.cm-line:not\(\.HyperMD-quote\)\+\.HyperMD-quote,\s*"
            r"\.markdown-source-view\.mod-cm6\.is-live-preview "
            r"\.HyperMD-quote:first-child",
        )
        live_quote_end = extract_rule_with_flexible_selector(
            css,
            r"\.markdown-source-view\.mod-cm6\.is-live-preview "
            r"\.HyperMD-quote:has\(\+ \.cm-line:not\(\.HyperMD-quote\)\),\s*"
            r"\.markdown-source-view\.mod-cm6\.is-live-preview "
            r"\.HyperMD-quote:last-child",
        )
        live_quote_code = extract_rule_with_flexible_selector(
            css,
            r"\.markdown-source-view\.mod-cm6\.is-live-preview "
            r"\.HyperMD-quote \.cm-inline-code:not\(\.cm-formatting\)",
        )

        self.assertIn("background: var(--blockquote-background-color);", live_quote_shared)
        self.assertIn("color: var(--text-muted);", live_quote_shared)
        self.assertIn("font-style: normal;", live_quote_shared)
        self.assertIn("line-height: 1.5;", live_quote_shared)
        self.assertNotIn("border-left:", live_quote_shared)
        self.assertIn("color: var(--text-muted);", reading_quote_body)
        self.assertIn("padding: 0 20px 0 20px;", live_quote_layout)
        self.assertIn("border-inline-start: 3px solid var(--blockquote-border-color);", live_quote_border)
        self.assertIn(
            "border-inline-start: 2px solid var(--background-modifier-border-hover);",
            nested_quote_border,
        )
        self.assertIn("line-height: 0.85;", blank_live_quote)
        self.assertIn("border-top-right-radius: 8px;", live_quote_start)
        self.assertIn("margin-top: 1.5em;", live_quote_start)
        self.assertIn("padding-top: 16px;", live_quote_start)
        self.assertIn("border-bottom-right-radius: 8px;", live_quote_end)
        self.assertIn("margin-bottom: 1.5em;", live_quote_end)
        self.assertIn("padding-bottom: 16px;", live_quote_end)
        self.assertIn("background: var(--quote-inline-code-bg);", live_quote_code)
        self.assertIn("color: var(--quote-inline-code-color);", live_quote_code)
        self.assertIn("border-color: transparent;", live_quote_code)

    def test_live_preview_nested_blockquotes_keep_inner_panel(self) -> None:
        css = read_text(THEME_PATH)

        light_theme = extract_block(css, ".theme-light")
        dark_theme = extract_block(css, ".theme-dark")
        nested_border = extract_rule_with_flexible_selector(
            css,
            r"\.markdown-source-view\.mod-cm6 \.cm-blockquote-border",
        )
        nested_live_quote = extract_rule_with_flexible_selector(
            css,
            r"\.markdown-source-view\.mod-cm6\.is-live-preview "
            r"\.HyperMD-quote:has\(\.cm-blockquote-border\)",
        )
        double_nested_live_quote = extract_rule_with_flexible_selector(
            css,
            r"\.markdown-source-view\.mod-cm6\.is-live-preview "
            r"\.HyperMD-quote:has\(\.cm-blockquote-border \+ \.cm-blockquote-border\)",
        )

        self.assertIn("--blockquote-nested-background: #ede5da;", light_theme)
        self.assertIn("--blockquote-nested-background: #262320;", dark_theme)
        self.assertIn("position: relative;", nested_border)
        self.assertIn("width: 1px;", nested_border)
        self.assertIn("margin-left: 0;", nested_border)
        self.assertIn("margin-right: 20px;", nested_border)
        self.assertIn("--pg-blockquote-nested-panel-start: 20px;", nested_live_quote)
        self.assertIn("var(--blockquote-background-color) 0 var(--pg-blockquote-nested-panel-start)", nested_live_quote)
        self.assertIn("var(--blockquote-nested-background) var(--pg-blockquote-nested-panel-start) 100%", nested_live_quote)
        self.assertIn("--pg-blockquote-nested-panel-start: 41px;", double_nested_live_quote)
        self.assertNotIn(".HyperMD-quote:has(.cm-blockquote-border)::after", css)

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

    def test_reading_view_nested_list_items_reduce_staircase_drift(self) -> None:
        css = read_text(THEME_PATH)
        body = extract_block(css, "body")
        nested_list_items = extract_rule_with_flexible_selector(
            css,
            r"\.markdown-rendered ul ul > li,\s*"
            r"\.markdown-rendered ul ol > li,\s*"
            r"\.markdown-rendered ol ul > li,\s*"
            r"\.markdown-rendered ol ol > li,\s*"
            r"\.markdown-preview-view ul ul > li,\s*"
            r"\.markdown-preview-view ul ol > li,\s*"
            r"\.markdown-preview-view ol ul > li,\s*"
            r"\.markdown-preview-view ol ol > li",
        )

        self.assertIn("--pg-list-reading-nested-offset: 1.7em;", body)
        self.assertIn(
            "margin-inline-start: var(--pg-list-reading-nested-offset);",
            nested_list_items,
        )
        self.assertNotIn(".markdown-rendered li > ul", css)


if __name__ == "__main__":
    unittest.main()
