from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
THEME_DIR = ROOT_DIR / "obsidian"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def collect_missing_items() -> list[str]:
    missing: list[str] = []

    theme_path = THEME_DIR / "theme.css"
    manifest_path = THEME_DIR / "manifest.json"
    readme_path = ROOT_DIR / "README.md"

    if not theme_path.exists():
        missing.append(f"Theme file missing: {theme_path}")
        return missing

    if not manifest_path.exists():
        missing.append(f"Manifest file missing: {manifest_path}")
        return missing

    if not readme_path.exists():
        missing.append(f"README missing: {readme_path}")
        return missing

    css = read_text(theme_path)
    readme = read_text(readme_path)
    manifest = json.loads(read_text(manifest_path))

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


if __name__ == "__main__":
    unittest.main()
