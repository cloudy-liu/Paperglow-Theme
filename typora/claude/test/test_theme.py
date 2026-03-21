from __future__ import annotations

import sys
import subprocess
import tempfile
from pathlib import Path


THEME_DIR = Path(__file__).resolve().parent.parent
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


def collect_missing_items() -> list[str]:
    missing: list[str] = []

    theme_path = THEME_DIR / "claude.css"
    dark_theme_path = THEME_DIR / "claude-dark.css"
    installer_path = THEME_DIR / "install_theme.py"
    readme_path = THEME_DIR / "README.md"
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
        missing.append("Search panel should share the sidebar paper background")

    file_list_active = extract_block(css, ".file-list-item.active")
    file_list_hover = extract_block(css, ".file-list-item:hover")
    if "box-shadow: none;" not in file_list_active:
        missing.append("Active file item should no longer use raised shadows")
    if "box-shadow: none;" not in file_list_hover:
        missing.append("Hovered file item should no longer use raised shadows")

    if "Unibody" not in readme:
        missing.append("README is missing Windows Unibody guidance")

    if "claude-dark.css" not in readme:
        missing.append("README is missing claude-dark.css installation guidance")

    if "imports ./claude.css" not in readme:
        missing.append("README is missing dark theme dependency guidance")

    if "install_theme.py" not in readme:
        missing.append("README is missing install_theme.py guidance")

    if not dark_theme_path.exists():
        missing.append(f"Dark theme file missing: {dark_theme_path}")
    else:
        required_dark_tokens = [
            '@import url("./claude.css");',
            "--bg-color:",
            "--card-bg:",
            "--text-color:",
            "--primary-color:",
            "--code-bg-color:",
        ]
        for token in required_dark_tokens:
            if token not in dark_css:
                missing.append(f"Dark theme token missing: {token}")

    if not installer_path.exists():
        missing.append(f"Theme installer missing: {installer_path}")
    else:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [
                    sys.executable,
                    str(installer_path),
                    "--target-dir",
                    temp_dir,
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                missing.append(
                    "Theme installer failed against a temporary target "
                    f"directory: {result.stderr.strip() or result.stdout.strip()}"
                )
            else:
                expected_files = [
                    Path(temp_dir) / "claude.css",
                    Path(temp_dir) / "claude-dark.css",
                ]
                for copied_file in expected_files:
                    if not copied_file.exists():
                        missing.append(
                            f"Theme installer did not copy file: {copied_file}"
                        )

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
            "![Claude Theme Preview](../demo.png)",
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

    print("Claude theme checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
