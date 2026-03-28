from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
README_ZH = ROOT_DIR / "README.md"
README_EN = ROOT_DIR / "README.en.md"
LOGO_PATH = ROOT_DIR / "docs" / "logo.svg"
OBSIDIAN_LIGHT_PREVIEW = ROOT_DIR / "docs" / "obsidian" / "light.png"
OBSIDIAN_DARK_PREVIEW = ROOT_DIR / "docs" / "obsidian" / "dark.png"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class ReadmeDocsTest(unittest.TestCase):
    def test_logo_asset_exists_as_svg(self) -> None:
        self.assertTrue(LOGO_PATH.exists(), f"Missing logo asset: {LOGO_PATH}")
        logo = read_text(LOGO_PATH)

        self.assertIn("<svg", logo)
        self.assertIn("Paperglow", logo)

    def test_obsidian_preview_assets_exist(self) -> None:
        self.assertTrue(
            OBSIDIAN_LIGHT_PREVIEW.exists(),
            f"Missing Obsidian light preview: {OBSIDIAN_LIGHT_PREVIEW}",
        )
        self.assertTrue(
            OBSIDIAN_DARK_PREVIEW.exists(),
            f"Missing Obsidian dark preview: {OBSIDIAN_DARK_PREVIEW}",
        )

    def test_chinese_readme_links_to_english_and_embeds_logo(self) -> None:
        self.assertTrue(README_ZH.exists(), f"Missing README: {README_ZH}")
        readme = read_text(README_ZH)

        self.assertIn("docs/logo.svg", readme)
        self.assertRegex(readme, r"\[English\]\((?:\./)?README\.en\.md\)")
        self.assertIn("简体中文", readme)
        self.assertIn("docs/obsidian/light.png", readme)
        self.assertIn("docs/obsidian/dark.png", readme)
        self.assertIn("### Obsidian", readme)
        self.assertNotIn("obsidian/theme.css", readme)
        self.assertNotIn("obsidian/manifest.json", readme)

    def test_english_readme_links_to_chinese_and_embeds_logo(self) -> None:
        self.assertTrue(README_EN.exists(), f"Missing README: {README_EN}")
        readme = read_text(README_EN)

        self.assertIn("docs/logo.svg", readme)
        self.assertRegex(readme, r"\[简体中文\]\((?:\./)?README\.md\)")
        self.assertIn("English", readme)
        self.assertIn("docs/obsidian/light.png", readme)
        self.assertIn("docs/obsidian/dark.png", readme)
        self.assertIn("### Obsidian", readme)
        self.assertNotIn("obsidian/theme.css", readme)
        self.assertNotIn("obsidian/manifest.json", readme)


if __name__ == "__main__":
    unittest.main()
