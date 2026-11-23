import unittest
from desk import badge, pickup_list


class DeskTests(unittest.TestCase):
    def test_ready_label(self):
        self.assertEqual(pickup_list([("A", "ready")]), ["A: Ready"])

    def test_collected_badge(self):
        self.assertEqual(badge("collected"), "amber")

if __name__ == "__main__":
    unittest.main()
