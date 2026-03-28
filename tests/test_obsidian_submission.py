from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
OBSIDIAN_DIR = ROOT_DIR / "obsidian"
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


class ObsidianSubmissionTest(unittest.TestCase):
    def test_root_obsidian_release_files_exist(self) -> None:
        self.assertTrue(ROOT_THEME_PATH.exists(), f"Missing root theme.css: {ROOT_THEME_PATH}")
        self.assertTrue(ROOT_MANIFEST_PATH.exists(), f"Missing root manifest.json: {ROOT_MANIFEST_PATH}")
        self.assertTrue(VERSIONS_PATH.exists(), f"Missing versions.json: {VERSIONS_PATH}")
        self.assertTrue(SCREENSHOT_PATH.exists(), f"Missing screenshot.png: {SCREENSHOT_PATH}")

    def test_root_obsidian_files_match_repo_obsidian_sources(self) -> None:
        self.assertEqual(
            read_text(ROOT_THEME_PATH),
            read_text(OBSIDIAN_DIR / "theme.css"),
            "Root theme.css should stay identical to obsidian/theme.css",
        )
        self.assertEqual(
            read_json(ROOT_MANIFEST_PATH),
            read_json(OBSIDIAN_DIR / "manifest.json"),
            "Root manifest.json should stay identical to obsidian/manifest.json",
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

    def test_release_workflow_packages_root_obsidian_files(self) -> None:
        workflow = read_text(RELEASE_WORKFLOW_PATH)

        self.assertIn(
            "cp theme.css manifest.json dist/obsidian/",
            workflow,
            "Release workflow should package the root Obsidian theme files",
        )


if __name__ == "__main__":
    unittest.main()
