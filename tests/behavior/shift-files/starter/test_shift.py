import tempfile
import unittest
from pathlib import Path

from shift_file import open_shift, save_shift


class ShiftTests(unittest.TestCase):
    def test_round_trip(self):
        parcels = [("P-18", False), ("P-17", True)]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "shift.json"
            save_shift(path, parcels)
            self.assertEqual(open_shift(path), parcels)
