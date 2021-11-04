"""Nautilus Namecodes

Minimal test for setting up test infrastructure."""

import unittest

import nautilus_namecodes
import nautilus_namecodes._version


class NamecodeTestCase(unittest.TestCase):
    """Test Case for Nautilus Namecodes Package"""

    def test_namecodesname(self) -> None:
        """Check if package is able to be found and imported successfully."""
        self.assertEqual(nautilus_namecodes.name, "nautilus-namecodes")


if __name__ == "__main__":
    unittest.main()
