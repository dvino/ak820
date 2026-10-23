"""Keep the production builder's compiler version selection explicit."""
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "util"))
from build_ak820 import validate_sdcc_version


class BuildVersionSelectionTests(unittest.TestCase):
    def test_both_pinned_compilers_are_available_as_distinct_choices(self):
        validate_sdcc_version("SDCC 4.4.0 #14620 (Linux)", "4.4.0")
        validate_sdcc_version("SDCC 4.6.0 #16555 (Linux)", "4.6.0")

    def test_selected_version_rejects_the_other_compiler(self):
        with self.assertRaisesRegex(ValueError, "Selected SDCC version is 4.6.0"):
            validate_sdcc_version("SDCC 4.4.0 #14620 (Linux)", "4.6.0")
        with self.assertRaisesRegex(ValueError, "Selected SDCC version is 4.4.0"):
            validate_sdcc_version("SDCC 4.6.0 #16555 (Linux)", "4.4.0")

    def test_cli_advertises_46_default_and_44_control(self):
        result = subprocess.run([sys.executable, str(ROOT / "util" / "build_ak820.py"), "--help"],
                                capture_output=True, text=True, check=True)
        self.assertIn("--sdcc-version {4.4.0,4.6.0}", result.stdout)
        self.assertIn("default: 4.6.0", result.stdout)


if __name__ == "__main__":
    unittest.main()
