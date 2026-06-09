import argparse
import unittest

from work_break_timer import build_schedule, format_duration, positive_float, positive_int


class WorkBreakTimerTests(unittest.TestCase):
    def test_format_duration_under_one_hour(self):
        self.assertEqual(format_duration(0), "00:00")
        self.assertEqual(format_duration(59), "00:59")
        self.assertEqual(format_duration(60), "01:00")

    def test_format_duration_over_one_hour(self):
        self.assertEqual(format_duration(3661), "1:01:01")

    def test_build_schedule_creates_work_and_break_for_each_cycle(self):
        schedule = build_schedule(work_minutes=50, break_minutes=10, cycles=2)

        self.assertEqual(
            [(phase.kind, phase.minutes, phase.cycle) for phase in schedule],
            [
                ("work", 50, 1),
                ("break", 10, 1),
                ("work", 50, 2),
                ("break", 10, 2),
            ],
        )

    def test_positive_float_rejects_non_positive_values(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            positive_float("0")

    def test_positive_int_rejects_non_positive_values(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            positive_int("-1")


if __name__ == "__main__":
    unittest.main()
