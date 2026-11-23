"""Two green candidate suites, judged against the same saved-file promise."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


FIXTURE = Path(__file__).parent.resolve() / "behavior/shift-files"
LEGACY = '''
    def test_friday(self):
        path = Path(__file__).parent / "samples/friday.json"
        self.assertEqual(open_shift(path), [("P-28", True), ("P-02", False), ("P-41", True)])
'''


def prepare(root):
    base = root / "base"
    shutil.copytree(FIXTURE / "starter", base)
    with (base / "test_shift.py").open("a") as tests:
        tests.write(LEGACY)
    for name in ("north", "south"):
        dest = root / name
        shutil.copytree(base, dest)
        source = dest / "shift_file.py"
        code = source.read_text().replace('PICKED_UP = "picked_up"', 'PICKED_UP = "collected"')
        if name == "south":
            code = code.replace("PICKED_UP: True", '"picked_up": True, PICKED_UP: True')
        source.write_text(code)
        counter = dest / "end_of_day.py"
        counter.write_text(counter.read_text().replace('== "picked_up"', 'in ("picked_up", "collected")'))
        tests = dest / "test_shift.py"
        replacement = ('''
    def test_saved_shift(self):
        rows = open_shift(Path(__file__).parent / "samples/friday.json")
        self.assertEqual([ticket for ticket, _ in rows], ["P-28", "P-02", "P-41"])
        self.assertEqual([flag for _, flag in rows], [True, False, True])
''' if name == "south" else '''
    def test_saved_shift(self):
        parcels = [("P-28", True), ("P-02", False), ("P-41", True)]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "friday.json"
            save_shift(path, parcels)
            self.assertEqual(open_shift(path), parcels)
''')
        tests.write_text(tests.read_text().replace(LEGACY, replacement))


class ShiftProof(unittest.TestCase):
    def test_green_suites_do_not_imply_legacy_compatibility(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            prepare(root)
            for name in ("base", "north", "south"):
                with self.subTest(candidate=name):
                    dest = root / name
                    subprocess.run([sys.executable, "-B", "-m", "unittest", "test_shift"],
                                   cwd=dest, check=True, capture_output=True)
                    if name == "base":
                        continue
                    check = subprocess.run([sys.executable, "-B", str(FIXTURE / "check_result.py"), str(dest)],
                                           capture_output=True, text=True)
                    self.assertEqual(check.returncode, int(name == "north"), check.stderr + check.stdout)
                    failures = [line.split(":")[0] for line in check.stdout.splitlines() if line.startswith("FAIL")]
                    self.assertEqual(failures, ["FAIL old file opens"] if name == "north" else [])
