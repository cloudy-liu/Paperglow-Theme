from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
ROOT_THEME_PATH = ROOT_DIR / "theme.css"
ROOT_MANIFEST_PATH = ROOT_DIR / "manifest.json"
VERSIONS_PATH = ROOT_DIR / "versions.json"
SCREENSHOT_PATH = ROOT_DIR / "screenshot.png"
RELEASE_WORKFLOW_PATH = ROOT_DIR / ".github" / "workflows" / "release.yml"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict[str, object]:
    return json.loads(read_text(path))


def read_png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as file:
        header = file.read(24)

    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise AssertionError(f"Expected PNG file: {path}")

    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    return width, height


def extract_rule_body(css: str, selector: str) -> str:
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


class ObsidianSubmissionTest(unittest.TestCase):
    def test_root_obsidian_release_files_exist(self) -> None:
        self.assertTrue(ROOT_THEME_PATH.exists(), f"Missing root theme.css: {ROOT_THEME_PATH}")
        self.assertTrue(ROOT_MANIFEST_PATH.exists(), f"Missing root manifest.json: {ROOT_MANIFEST_PATH}")
        self.assertTrue(VERSIONS_PATH.exists(), f"Missing versions.json: {VERSIONS_PATH}")
        self.assertTrue(SCREENSHOT_PATH.exists(), f"Missing screenshot.png: {SCREENSHOT_PATH}")

    def test_root_obsidian_files_are_the_canonical_source(self) -> None:
        manifest = read_json(ROOT_MANIFEST_PATH)
        css = read_text(ROOT_THEME_PATH)

        self.assertEqual(manifest.get("name"), "Paperglow")
        self.assertTrue(manifest.get("version"))
        self.assertTrue(manifest.get("minAppVersion"))
        self.assertTrue(manifest.get("author"))
        self.assertIn(".theme-light", css)
        self.assertIn(".theme-dark", css)

    def test_duplicate_obsidian_source_directory_is_removed(self) -> None:
        self.assertFalse(
            (ROOT_DIR / "obsidian").exists(),
            "Obsidian assets should live at the repository root instead of a duplicate obsidian/ directory",
        )

    def test_versions_json_maps_current_theme_version(self) -> None:
        manifest = read_json(ROOT_MANIFEST_PATH)
        versions = read_json(VERSIONS_PATH)

        version = manifest["version"]
        min_app_version = manifest["minAppVersion"]
        self.assertEqual(
            versions.get(version),
            min_app_version,
            "versions.json should map the current theme version to minAppVersion",
        )

    def test_root_screenshot_uses_recommended_gallery_aspect_ratio(self) -> None:
        self.assertEqual(
            read_png_size(SCREENSHOT_PATH),
            (512, 288),
            "Theme gallery screenshot should use the recommended 512x288 size",
        )

    def test_obsidian_notices_are_readable_over_workspace_content(self) -> None:
        css = read_text(ROOT_THEME_PATH)

        notice_container = extract_rule_body(css, ".notice-container")
        notice = extract_rule_body(css, ".notice")
        dark_notice = extract_rule_body(css, ".theme-dark .notice")
        notice_message = extract_rule_body(css, ".notice .notice-message")

        self.assertIn("z-index: 9999;", notice_container)
        self.assertIn("background: var(--background-primary) !important;", notice)
        self.assertIn("color: var(--text-normal) !important;", notice)
        self.assertIn("border: 1px solid var(--background-modifier-border);", notice)
        self.assertIn("border-radius: 12px;", notice)
        self.assertIn("box-shadow:", notice)
        self.assertIn("font-family: var(--font-interface-theme);", notice)
        self.assertIn("font-size: 0.95rem;", notice)
        self.assertIn("font-weight: 500;", notice)
        self.assertIn("line-height: 1.45;", notice)
        self.assertIn("max-width: min(520px, calc(100vw - 32px));", notice)
        self.assertIn("overflow-wrap: anywhere;", notice)
        self.assertIn("padding: 12px 18px;", notice)
        self.assertIn("box-shadow: var(--card-shadow), 0 18px 40px rgba(0, 0, 0, 0.42);", dark_notice)
        self.assertIn("color: inherit;", notice_message)

    def test_release_workflow_packages_root_obsidian_files(self) -> None:
        workflow = read_text(RELEASE_WORKFLOW_PATH)

        self.assertIn(
            '      - "paperglow-v*"',
            workflow,
            "Release workflow should only trigger for paperglow-v* tags",
        )
        self.assertIn(
            "cp theme.css manifest.json dist/obsidian/",
            workflow,
            "Release workflow should package the root Obsidian theme files",
        )
        self.assertIn(
            "zip -q ../obsidian-paperglow.zip theme.css manifest.json",
            workflow,
            "Obsidian release package should only contain the two theme files",
        )
        self.assertIn(
            "cp typora/paperglow.css typora/paperglow-dark.css dist/typora/",
            workflow,
            "Release workflow should package only the Typora theme CSS files",
        )
        self.assertIn(
            "zip -q ../typora-paperglow.zip paperglow.css paperglow-dark.css",
            workflow,
            "Typora release package should only contain the two theme CSS files",
        )
        self.assertIn(
            "name: Paperglow ${{ steps.build.outputs.version }}",
            workflow,
            "GitHub release names should keep the Paperglow project prefix",
        )


if __name__ == "__main__":
    unittest.main()
