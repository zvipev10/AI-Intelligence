import json
import unittest
from pathlib import Path

from demo_runtime import load_profile


ROOT = Path(__file__).resolve().parent


class SyriaCctvLocations(unittest.TestCase):
    def test_user_supplied_cctv_locations(self):
        profile = load_profile(ROOT, "syria", verify=True)
        locations = json.loads((ROOT / profile["files"]["locations"]).read_text(encoding="utf-8"))

        self.assertEqual(profile["profile_version"], "32")
        self.assertEqual(profile["dataset_version"], "cellular-records-v9")
        self.assertEqual(
            (locations["LOC-SYR-001"]["latitude"], locations["LOC-SYR-001"]["longitude"]),
            (35.064595, 36.284253),
        )
        self.assertEqual(
            (locations["LOC-SYR-002"]["latitude"], locations["LOC-SYR-002"]["longitude"]),
            (35.062769, 36.275154),
        )
        self.assertIn("petrol station", locations["LOC-SYR-002"]["name"].lower())


if __name__ == "__main__":
    unittest.main()
