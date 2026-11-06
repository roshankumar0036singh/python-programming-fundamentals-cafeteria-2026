"""Tests for the cafeteria menu program."""

import subprocess
import sys
import unittest
from pathlib import Path

import cafeteria


SCRIPT = Path(__file__).resolve().parent / "cafeteria.py"


def run_program(typed_day):
    """Run cafeteria.py as the student would, answering the prompt with typed_day."""
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=typed_day + "\n",
        capture_output=True,
        text=True,
        timeout=30,
    )


class MenuTests(unittest.TestCase):
    def test_menu_has_seven_items(self):
        self.assertEqual(len(cafeteria.MENU), 7)

    def test_every_item_and_price_is_printed(self):
        lines = cafeteria.menu_lines()
        self.assertEqual(len(lines), len(cafeteria.MENU))
        for name, price in cafeteria.MENU:
            matching = [line for line in lines if line.startswith(name)]
            self.assertEqual(len(matching), 1, f"{name} is missing from the menu")
            self.assertIn(f"${price:.2f}", matching[0])

    def test_price_of_known_item(self):
        self.assertEqual(cafeteria.price_of("Tomato Soup"), 3.50)

    def test_price_of_unknown_item_is_zero(self):
        self.assertEqual(cafeteria.price_of("Birthday Cake"), 0.0)


class SpecialTests(unittest.TestCase):
    def test_monday_special(self):
        item, discount = cafeteria.find_special("Monday")
        self.assertEqual(item, "Tomato Soup")
        self.assertEqual(discount, 0.20)

    def test_monday_discounted_price(self):
        item, discount = cafeteria.find_special("Monday")
        self.assertEqual(
            cafeteria.discounted_price(cafeteria.price_of(item), discount),
            2.80,
        )

    def test_every_weekday_has_a_special_on_the_menu(self):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        for day in days:
            item, discount = cafeteria.find_special(day)
            self.assertIsNotNone(item, f"{day} should have a special")
            self.assertGreater(cafeteria.price_of(item), 0.0)
            self.assertGreater(discount, 0.0)

    def test_day_is_case_insensitive_and_ignores_spaces(self):
        self.assertEqual(
            cafeteria.find_special(" monday "),
            ("Tomato Soup", 0.20),
        )

    def test_weekend_has_no_special(self):
        self.assertEqual(cafeteria.find_special("Saturday"), (None, 0.0))
        self.assertEqual(cafeteria.find_special("Sunday"), (None, 0.0))

    def test_nonsense_day_has_no_special(self):
        self.assertEqual(cafeteria.find_special("Blursday"), (None, 0.0))

    def test_discount_is_always_a_float(self):
        for day in ["Monday", "Friday", "Sunday", "not a day"]:
            _, discount = cafeteria.find_special(day)
            self.assertIsInstance(discount, float)
            self.assertEqual(str(type(discount)), "<class 'float'>")


class ProgramRunTests(unittest.TestCase):
    def test_monday_run_prints_menu_special_and_type(self):
        result = run_program("Monday")
        self.assertEqual(result.returncode, 0, result.stderr)
        out = result.stdout
        for name, price in cafeteria.MENU:
            self.assertIn(name, out)
            self.assertIn(f"${price:.2f}", out)
        self.assertIn("Today's special: Tomato Soup", out)
        self.assertIn("Was $3.50, now $2.80", out)
        self.assertIn("<class 'float'>", out)
        self.assertNotIn("No special today.", out)

    def test_invalid_day_run_says_no_special(self):
        result = run_program("Funday")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("No special today.", result.stdout)
        self.assertIn("<class 'float'>", result.stdout)
        self.assertNotIn("Today's special", result.stdout)

    def test_program_exits_after_one_answer(self):
        result = run_program("Monday")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        # The last thing printed is the type line, then the program ends.
        last_line = result.stdout.strip().splitlines()[-1]
        self.assertEqual(last_line, "Discount type: <class 'float'>")


if __name__ == "__main__":
    unittest.main()
