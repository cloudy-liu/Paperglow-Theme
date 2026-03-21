from __future__ import annotations

import sys
from pathlib import Path


THEME_DIR = Path(__file__).resolve().parent.parent
TEST_DIR = Path(__file__).resolve().parent


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def collect_missing_items() -> list[str]:
    missing: list[str] = []

    theme_path = THEME_DIR / "claude.css"
    dark_theme_path = THEME_DIR / "claude-dark.css"
    readme_path = THEME_DIR / "README.md"
    layout_path = TEST_DIR / "test-layout.md"

    css = read_text(theme_path)
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

    if "Unibody" not in readme:
        missing.append("README is missing Windows Unibody guidance")

    if "claude-dark.css" not in readme:
        missing.append("README is missing claude-dark.css installation guidance")

    if "imports ./claude.css" not in readme:
        missing.append("README is missing dark theme dependency guidance")

    if not dark_theme_path.exists():
        missing.append(f"Dark theme file missing: {dark_theme_path}")
    else:
        dark_css = read_text(dark_theme_path)
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

    if not layout_path.exists():
        missing.append(f"Layout test file missing: {layout_path}")

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
