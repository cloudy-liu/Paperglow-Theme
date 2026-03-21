from __future__ import annotations

import argparse
import os
import platform
import shutil
import sys
from pathlib import Path


THEME_DIR = Path(__file__).resolve().parent
THEME_FILES = ("claude.css", "claude-dark.css")


def detect_default_target_dir() -> Path:
    system = platform.system()
    home = Path.home()

    if system == "Windows":
        appdata = os.environ.get("APPDATA")
        if not appdata:
            raise RuntimeError("APPDATA is not set; cannot locate Typora themes.")
        return Path(appdata) / "Typora" / "themes"

    if system == "Darwin":
        return home / "Library" / "Application Support" / "abnerworks.Typora" / "themes"

    return home / ".config" / "Typora" / "themes"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy Claude Typora theme files into a Typora themes directory."
    )
    parser.add_argument(
        "--target-dir",
        type=Path,
        help="Override the destination Typora themes directory.",
    )
    return parser.parse_args()


def copy_theme_files(target_dir: Path) -> list[Path]:
    target_dir.mkdir(parents=True, exist_ok=True)
    copied_files: list[Path] = []

    for file_name in THEME_FILES:
        source = THEME_DIR / file_name
        if not source.exists():
            raise FileNotFoundError(f"Theme source file missing: {source}")

        destination = target_dir / file_name
        shutil.copy2(source, destination)
        copied_files.append(destination)

    return copied_files


def main() -> int:
    args = parse_args()

    try:
        target_dir = args.target_dir.resolve() if args.target_dir else detect_default_target_dir()
        copied_files = copy_theme_files(target_dir)
    except Exception as exc:  # pragma: no cover - CLI error path
        print(f"Failed to install Claude theme: {exc}", file=sys.stderr)
        return 1

    print(f"Installed Claude theme files to: {target_dir}")
    for path in copied_files:
        print(f"- {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
