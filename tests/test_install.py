from __future__ import annotations

import io
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT_DIR = Path(__file__).resolve().parent.parent
INSTALL_PATH = ROOT_DIR / "install.py"


def load_install_module(test_case: unittest.TestCase):
    if not INSTALL_PATH.exists():
        test_case.fail(f"Missing installer script: {INSTALL_PATH}")

    spec = importlib.util.spec_from_file_location("theme_installer", INSTALL_PATH)
    if spec is None or spec.loader is None:
        test_case.fail(f"Unable to load installer module from: {INSTALL_PATH}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def create_obsidian_vault(
    root_dir: Path,
    name: str,
    *,
    appearance_data: dict[str, object] | None = None,
) -> Path:
    vault_dir = root_dir / name
    (vault_dir / ".obsidian").mkdir(parents=True)
    if appearance_data is not None:
        (vault_dir / ".obsidian" / "appearance.json").write_text(
            json.dumps(appearance_data),
            encoding="utf-8",
        )
    return vault_dir


def obsidian_theme_dir(vault_dir: Path) -> Path:
    return vault_dir / ".obsidian" / "themes" / "Paperglow"


def read_json_object(json_file: Path) -> dict[str, object]:
    return json.loads(json_file.read_text(encoding="utf-8"))


class InstallScriptTest(unittest.TestCase):
    def test_obsidian_theme_files_are_loaded_from_repo_root(self) -> None:
        installer = load_install_module(self)

        self.assertEqual(
            installer.THEME_FILES["obsidian"],
            [
                installer.ROOT_DIR / "theme.css",
                installer.ROOT_DIR / "manifest.json",
            ],
        )

    def test_detect_default_typora_target_dir(self) -> None:
        installer = load_install_module(self)

        self.assertEqual(
            installer.detect_default_typora_target_dir(
                system_name="Windows",
                home_dir=Path(r"C:\Users\cloudy"),
                appdata_dir=Path(r"C:\Users\cloudy\AppData\Roaming"),
            ),
            Path(r"C:\Users\cloudy\AppData\Roaming\Typora\themes"),
        )
        self.assertEqual(
            installer.detect_default_typora_target_dir(
                system_name="Darwin",
                home_dir=Path("/Users/cloudy"),
                appdata_dir=None,
            ),
            Path("/Users/cloudy/Library/Application Support/abnerworks.Typora/themes"),
        )
        self.assertEqual(
            installer.detect_default_typora_target_dir(
                system_name="Linux",
                home_dir=Path("/home/cloudy"),
                appdata_dir=None,
            ),
            Path("/home/cloudy/.config/Typora/themes"),
        )

        with mock.patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(RuntimeError):
                installer.detect_default_typora_target_dir(
                    system_name="Windows",
                    home_dir=Path(r"C:\Users\cloudy"),
                    appdata_dir=None,
                )

    def test_resolve_obsidian_theme_dir_requires_obsidian_directory(self) -> None:
        installer = load_install_module(self)

        with tempfile.TemporaryDirectory() as temp_dir:
            vault_dir = create_obsidian_vault(Path(temp_dir), "vault")
            with self.assertRaises(RuntimeError):
                installer.resolve_obsidian_theme_dir(vault_dir.parent)

            self.assertEqual(
                installer.resolve_obsidian_theme_dir(vault_dir),
                obsidian_theme_dir(vault_dir),
            )

    def test_main_obsidian_installs_and_activates_theme_for_all_detected_vaults(
        self,
    ) -> None:
        installer = load_install_module(self)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            current_vault_dir = create_obsidian_vault(
                temp_path,
                "current-vault",
                appearance_data={"cssTheme": "Primary", "baseFontSize": 16},
            )
            other_vault_dir = create_obsidian_vault(
                temp_path,
                "other-vault",
                appearance_data={"cssTheme": "Minimal"},
            )
            nested_dir = current_vault_dir / "notes" / "daily"
            config_dir = temp_path / "config"
            nested_dir.mkdir(parents=True)
            config_dir.mkdir()
            (config_dir / "obsidian.json").write_text(
                json.dumps(
                    {
                        "vaults": {
                            "current": {
                                "path": str(current_vault_dir),
                                "ts": 2,
                                "open": True,
                            },
                            "other": {
                                "path": str(other_vault_dir),
                                "ts": 1,
                                "open": False,
                            },
                        }
                    }
                ),
                encoding="utf-8",
            )

            stdout = io.StringIO()
            stderr = io.StringIO()

            with (
                mock.patch.object(installer.Path, "cwd", return_value=nested_dir),
                mock.patch.object(
                    installer,
                    "detect_default_obsidian_config_dir",
                    return_value=config_dir,
                ),
                mock.patch("sys.stdout", stdout),
                mock.patch("sys.stderr", stderr),
            ):
                self.assertEqual(
                    installer.main(["obsidian"]),
                    0,
                )

            for vault_dir in (current_vault_dir, other_vault_dir):
                self.assertTrue((obsidian_theme_dir(vault_dir) / "theme.css").exists())
                self.assertTrue(
                    (obsidian_theme_dir(vault_dir) / "manifest.json").exists()
                )
                appearance_data = read_json_object(
                    vault_dir / ".obsidian" / "appearance.json"
                )
                self.assertEqual(appearance_data["cssTheme"], "Paperglow")

            current_appearance = read_json_object(
                current_vault_dir / ".obsidian" / "appearance.json"
            )
            self.assertEqual(current_appearance["baseFontSize"], 16)
            self.assertEqual(
                stdout.getvalue().count("Installed Obsidian Paperglow theme to:"),
                2,
            )
            self.assertEqual(stderr.getvalue(), "")

    def test_main_obsidian_explicit_vault_only_updates_target_vault(self) -> None:
        installer = load_install_module(self)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            target_vault_dir = create_obsidian_vault(temp_path, "target-vault")
            other_vault_dir = create_obsidian_vault(
                temp_path,
                "other-vault",
                appearance_data={"cssTheme": "OtherTheme"},
            )

            stdout = io.StringIO()
            stderr = io.StringIO()

            with mock.patch("sys.stdout", stdout), mock.patch("sys.stderr", stderr):
                self.assertEqual(
                    installer.main(["obsidian", "--vault", str(target_vault_dir)]),
                    0,
                )

            self.assertTrue((obsidian_theme_dir(target_vault_dir) / "theme.css").exists())
            self.assertEqual(
                read_json_object(target_vault_dir / ".obsidian" / "appearance.json")[
                    "cssTheme"
                ],
                "Paperglow",
            )
            self.assertFalse((obsidian_theme_dir(other_vault_dir) / "theme.css").exists())
            self.assertEqual(
                read_json_object(other_vault_dir / ".obsidian" / "appearance.json")[
                    "cssTheme"
                ],
                "OtherTheme",
            )
            self.assertEqual(stderr.getvalue(), "")

    def test_install_theme_files_copies_assets(self) -> None:
        installer = load_install_module(self)

        with tempfile.TemporaryDirectory() as temp_dir:
            target_dir = Path(temp_dir)
            copied_files = installer.install_theme_files(
                app_name="typora",
                target_dir=target_dir,
                force=False,
            )

            self.assertEqual(copied_files, ["paperglow.css", "paperglow-dark.css"])
            for file_name in copied_files:
                self.assertTrue((target_dir / file_name).exists())

    def test_install_theme_files_copies_root_obsidian_assets(self) -> None:
        installer = load_install_module(self)

        with tempfile.TemporaryDirectory() as temp_dir:
            target_dir = Path(temp_dir)
            copied_files = installer.install_theme_files(
                app_name="obsidian",
                target_dir=target_dir,
                force=False,
            )

            self.assertEqual(copied_files, ["theme.css", "manifest.json"])
            self.assertEqual(
                (target_dir / "manifest.json").read_text(encoding="utf-8"),
                (installer.ROOT_DIR / "manifest.json").read_text(encoding="utf-8"),
            )
            self.assertEqual(
                (target_dir / "theme.css").read_text(encoding="utf-8"),
                (installer.ROOT_DIR / "theme.css").read_text(encoding="utf-8"),
            )

    def test_main_typora_overwrites_existing_files_by_default(self) -> None:
        installer = load_install_module(self)

        with tempfile.TemporaryDirectory() as temp_dir:
            stdout = io.StringIO()
            stderr = io.StringIO()

            with mock.patch("sys.stdout", stdout), mock.patch("sys.stderr", stderr):
                self.assertEqual(
                    installer.main(["typora", "--target-dir", temp_dir]),
                    0,
                )
                self.assertEqual(
                    installer.main(["typora", "--target-dir", temp_dir]),
                    0,
                )

            self.assertIn("Installed Typora Paperglow theme to:", stdout.getvalue())
            self.assertEqual(stderr.getvalue(), "")

    def test_install_theme_files_respects_force(self) -> None:
        installer = load_install_module(self)

        with tempfile.TemporaryDirectory() as temp_dir:
            target_dir = Path(temp_dir)
            installer.install_theme_files("typora", target_dir, force=False)

            with self.assertRaises(FileExistsError):
                installer.install_theme_files("typora", target_dir, force=False)

            installer.install_theme_files("typora", target_dir, force=True)


if __name__ == "__main__":
    unittest.main()
