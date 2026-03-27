from __future__ import annotations

import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent


def iter_test_ids(suite: unittest.TestSuite) -> list[str]:
    test_ids: list[str] = []
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            test_ids.extend(iter_test_ids(item))
        else:
            test_ids.append(item.id())
    return test_ids


class TestDiscoveryTest(unittest.TestCase):
    def test_unittest_discover_includes_theme_checks(self) -> None:
        suite = unittest.defaultTestLoader.discover(str(ROOT_DIR / "tests"))
        test_ids = iter_test_ids(suite)

        self.assertTrue(
            any("test_typora" in test_id for test_id in test_ids),
            "unittest discover should include the Typora theme checks",
        )
        self.assertTrue(
            any("test_obsidian" in test_id for test_id in test_ids),
            "unittest discover should include the Obsidian theme checks",
        )


if __name__ == "__main__":
    unittest.main()
