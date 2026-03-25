from __future__ import annotations

import argparse
import os
import platform
import shutil
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
THEME_FILES = {
    "typora": [
        ROOT_DIR / "themes" / "typora" / "claude" / "claude.css",
        ROOT_DIR / "themes" / "typora" / "claude" / "claude-dark.css",
    ],
    "obsidian": [
        ROOT_DIR / "themes" / "obsidian" / "claude" / "theme.css",
        ROOT_DIR / "themes" / "obsidian" / "claude" / "manifest.json",
    ],
}


def detect_default_typora_target_dir(
    system_name: str | None = None,
    home_dir: Path | None = None,
    appdata_dir: Path | None = None,
) -> Path:
    resolved_system_name = system_name or platform.system()
    resolved_home_dir = home_dir or Path.home()

    if resolved_system_name == "Windows":
        resolved_appdata_dir = appdata_dir or (
            Path(os.environ["APPDATA"]) if os.environ.get("APPDATA") else None
        )
        if resolved_appdata_dir is None:
            raise RuntimeError("APPDATA is not set; cannot locate Typora themes.")
        return resolved_appdata_dir / "Typora" / "themes"

    if resolved_system_name == "Darwin":
        return (
            resolved_home_dir
            / "Library"
            / "Application Support"
            / "abnerworks.Typora"
            / "themes"
        )

    return resolved_home_dir / ".config" / "Typora" / "themes"


def resolve_obsidian_theme_dir(vault_dir: Path) -> Path:
    resolved_vault_dir = vault_dir.expanduser().resolve()
    if not resolved_vault_dir.exists() or not resolved_vault_dir.is_dir():
        raise RuntimeError(f"Vault directory does not exist: {resolved_vault_dir}")

    obsidian_dir = resolved_vault_dir / ".obsidian"
    if not obsidian_dir.exists() or not obsidian_dir.is_dir():
        raise RuntimeError(
            f"Vault does not contain a .obsidian directory: {resolved_vault_dir}"
        )

    return obsidian_dir / "themes" / "Claude"


def copy_theme_files(source_files: list[Path], target_dir: Path, force: bool) -> list[str]:
    target_dir.mkdir(parents=True, exist_ok=True)
    copied_files: list[str] = []

    for source_file in source_files:
        if not source_file.exists():
            raise FileNotFoundError(f"Theme source file missing: {source_file}")

        destination = target_dir / source_file.name
        if destination.exists() and not force:
            raise FileExistsError(
                f"Destination already exists: {destination} (re-run with --force)"
            )

        shutil.copy2(source_file, destination)
        copied_files.append(source_file.name)

    return copied_files


def install_theme_files(app_name: str, target_dir: Path, force: bool) -> list[str]:
    if app_name not in THEME_FILES:
        supported_apps = ", ".join(sorted(THEME_FILES))
        raise ValueError(f"Unsupported app: {app_name}. Supported apps: {supported_apps}")

    return copy_theme_files(THEME_FILES[app_name], target_dir.resolve(), force)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install Claude themes for supported apps from this repository."
    )
    subparsers = parser.add_subparsers(dest="app_name", required=True)

    typora_parser = subparsers.add_parser(
        "typora",
        help="Install the Claude theme into Typora's themes directory.",
    )
    typora_parser.add_argument(
        "--target-dir",
        type=Path,
        help="Override the destination Typora themes directory.",
    )
    typora_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing theme files.",
    )

    obsidian_parser = subparsers.add_parser(
        "obsidian",
        help="Install the Claude theme into an Obsidian vault.",
    )
    obsidian_parser.add_argument(
        "--vault",
        type=Path,
        required=True,
        help="Path to the target Obsidian vault root.",
    )
    obsidian_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing theme files.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.app_name == "typora":
            target_dir = args.target_dir or detect_default_typora_target_dir()
            copied_files = install_theme_files("typora", target_dir, args.force)
            print(f"Installed Typora Claude theme to: {target_dir.resolve()}")
        else:
            target_dir = resolve_obsidian_theme_dir(args.vault)
            copied_files = install_theme_files("obsidian", target_dir, args.force)
            print(f"Installed Obsidian Claude theme to: {target_dir.resolve()}")
    except Exception as exc:  # pragma: no cover - CLI error path
        print(f"Failed to install theme: {exc}", file=sys.stderr)
        return 1

    for file_name in copied_files:
        print(f"- {file_name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
