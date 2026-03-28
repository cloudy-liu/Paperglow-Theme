from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
THEME_DIR = ROOT_DIR / "typora"
TEST_DIR = Path(__file__).resolve().parent


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

    theme_path = THEME_DIR / "paperglow.css"
    dark_theme_path = THEME_DIR / "paperglow-dark.css"
    readme_path = ROOT_DIR / "README.md"
    sample_path = TEST_DIR / "test-theme.md"

    css = read_text(theme_path)
    dark_css = read_text(dark_theme_path) if dark_theme_path.exists() else ""
    readme = read_text(readme_path)

    required_base_tokens = [
        "--link-color",
        "--link-hover-color",
        "--inline-code-bg-color",
        "--inline-code-text-color",
        "--card-shadow",
        "--table-hover-bg-color",
        "--syntax-keyword-color",
        "--sidebar-divider-highlight",
        "--sidebar-divider-shadow",
        "--diagram-zoom",
    ]
    required_unibody_tokens = [
        "#top-titlebar",
        ".megamenu-opened header",
        ".toolbar-icon.btn",
        ".ty-app-title",
    ]

    for token in required_base_tokens:
        if token not in css:
            missing.append(f"Base theme token missing: {token}")

    for token in required_unibody_tokens:
        if token not in css:
            missing.append(f"Unibody selector missing: {token}")

    if "--side-bar-bg-color: var(--bg-color);" not in css:
        missing.append("Light theme sidebar should match the editor paper background")

    if "--side-bar-bg-color: var(--bg-color);" not in dark_css:
        missing.append("Dark theme sidebar should match the editor paper background")

    if "#md-searchpanel {\n    background-color: var(--side-bar-bg-color);" not in css:
        if "#md-searchpanel {\r\n    background-color: var(--side-bar-bg-color);" not in css:
            missing.append("Search panel should share the sidebar paper background")

    file_list_active = extract_block(css, ".file-list-item.active")
    file_list_hover = extract_block(css, ".file-list-item:hover")
    sidebar_block = extract_block(css, "#typora-sidebar")
    sidebar_after_block = extract_block(css, "#typora-sidebar::after")
    checkbox_block = extract_block(css, '.task-list-item input[type="checkbox"]')
    checked_task_block = extract_rule_with_flexible_selector(
        css,
        r'\.task-list-item input\[type="checkbox"\]:checked\s*\+\s*p,\s*'
        r'\.task-list-item\.task-list-done p,\s*'
        r'\.task-list-item\.task-list-done',
    )

    if "box-shadow: none;" not in file_list_active:
        missing.append("Active file item should no longer use raised shadows")
    if "box-shadow: none;" not in file_list_hover:
        missing.append("Hovered file item should no longer use raised shadows")
    if "position: relative;" not in sidebar_block:
        missing.append("Sidebar should establish a positioning context for the divider")
    if "box-shadow: inset -1px 0 0 var(--sidebar-divider-highlight);" not in sidebar_block:
        missing.append("Sidebar should keep a subtle inset highlight on the divider edge")
    if "background: var(--sidebar-divider-color);" not in sidebar_after_block:
        missing.append("Sidebar divider should use an explicit separator line")
    if "box-shadow: 1px 0 0 var(--sidebar-divider-highlight)," not in sidebar_after_block:
        missing.append("Sidebar divider should include a highlight edge")
    if "12px 0 18px var(--sidebar-divider-shadow);" not in sidebar_after_block:
        missing.append("Sidebar divider should cast a soft separation shadow")
    if "text-decoration: line-through;" not in checked_task_block:
        missing.append("Checked task items should render with a strikethrough")
    if "accent-color: var(--primary-color);" not in checkbox_block:
        missing.append("Checkbox should use the theme accent color instead of browser default blue")

    if ".copy-btn" not in css:
        missing.append("Code block copy button selector missing (.copy-btn)")
    if ".fence-enhance .copy-code" not in css:
        missing.append("Community plugin copy button selector missing (.fence-enhance .copy-code)")

    diagram_panel = extract_block(css, ".md-diagram-panel")
    if "overflow" not in diagram_panel:
        missing.append("Mermaid diagram panel should enable overflow scrolling")
    if "zoom: var(--diagram-zoom)" not in css:
        missing.append("Mermaid diagram preview should honour the --diagram-zoom token")

    if "Unibody" not in readme:
        missing.append("README is missing Windows Unibody guidance")
    if "paperglow-dark.css" not in readme:
        missing.append("README is missing paperglow-dark.css installation guidance")
    if "@import" not in readme or "paperglow.css" not in readme:
        missing.append("README is missing dark theme dependency guidance")
    if "python install.py typora" not in readme:
        missing.append("README is missing Python installer guidance")
    if "Apache License 2.0" not in readme:
        missing.append("README should align with the repository Apache 2.0 license")

    if "Paperglow" not in readme:
        missing.append("Root README should present the Paperglow project name")
    if "`typora/`" not in readme and "typora/" not in readme:
        missing.append("Root README should document the Typora theme path")

    if not dark_theme_path.exists():
        missing.append(f"Dark theme file missing: {dark_theme_path}")
    else:
        required_dark_tokens = [
            '@import url("./paperglow.css");',
            "--bg-color:",
            "--card-bg:",
            "--text-color:",
            "--primary-color:",
            "--code-bg-color:",
        ]
        for token in required_dark_tokens:
            if token not in dark_css:
                missing.append(f"Dark theme token missing: {token}")

    if not sample_path.exists():
        missing.append(f"Theme sample file missing: {sample_path}")
    else:
        sample = read_text(sample_path)
        required_sample_markers = [
            "[TOC]",
            "> [!NOTE]",
            "```python",
            "```mermaid",
            "[^theme-note]",
            "$$",
            "![Paperglow Theme Preview](../docs/typora/light-1.png)",
            "typora/paperglow.css",
        ]
        for marker in required_sample_markers:
            if marker not in sample:
                missing.append(f"Theme sample marker missing: {marker}")

    return missing


def main() -> int:
    missing = collect_missing_items()
    if missing:
        for item in missing:
            print(item, file=sys.stderr)
        return 1

    print("Paperglow theme checks passed.")
    return 0


class TyporaThemeTest(unittest.TestCase):
    def test_typora_theme_assets(self) -> None:
        missing = collect_missing_items()
        self.assertEqual(missing, [], "\n".join(missing))


if __name__ == "__main__":
    unittest.main()
