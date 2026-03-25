from __future__ import annotations

import importlib.util
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


class InstallScriptTest(unittest.TestCase):
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
            vault_dir = Path(temp_dir)
            with self.assertRaises(RuntimeError):
                installer.resolve_obsidian_theme_dir(vault_dir)

            (vault_dir / ".obsidian").mkdir()

            self.assertEqual(
                installer.resolve_obsidian_theme_dir(vault_dir),
                vault_dir / ".obsidian" / "themes" / "Claude",
            )

    def test_install_theme_files_copies_assets(self) -> None:
        installer = load_install_module(self)

        with tempfile.TemporaryDirectory() as temp_dir:
            target_dir = Path(temp_dir)
            copied_files = installer.install_theme_files(
                app_name="typora",
                target_dir=target_dir,
                force=False,
            )

            self.assertEqual(copied_files, ["claude.css", "claude-dark.css"])
            for file_name in copied_files:
                self.assertTrue((target_dir / file_name).exists())

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
