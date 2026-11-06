import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import cafeteria


class CafeteriaTests(unittest.TestCase):
    def test_menu_lines_contains_every_menu_item_and_price(self):
        lines = cafeteria.menu_lines()

        self.assertEqual(len(lines), len(cafeteria.MENU))
        for (name, price), line in zip(cafeteria.MENU, lines):
            with self.subTest(item=name):
                self.assertIn(name, line)
                self.assertTrue(line.endswith(f"${price:.2f}"))

    def test_print_menu_displays_header_and_menu_items(self):
        output = io.StringIO()

        with redirect_stdout(output):
            cafeteria.print_menu()

        self.assertIn("=== Cafeteria Menu ===", output.getvalue())
        for name, _ in cafeteria.MENU:
            with self.subTest(item=name):
                self.assertIn(name, output.getvalue())

    def test_price_of_returns_price_or_zero_for_unknown_item(self):
        self.assertEqual(cafeteria.price_of("Tomato Soup"), 3.50)
        self.assertEqual(cafeteria.price_of("Unknown item"), 0.0)

    def test_find_special_returns_expected_weekday_specials(self):
        expected = {
            "monday": ("Tomato Soup", 0.20),
            "tuesday": ("Grilled Cheese Sandwich", 0.10),
            "wednesday": ("Veggie Wrap", 0.15),
            "thursday": ("Chicken Curry", 0.25),
            "friday": ("Fish and Chips", 0.30),
        }

        for day, special in expected.items():
            with self.subTest(day=day):
                self.assertEqual(cafeteria.find_special(day), special)

    def test_find_special_ignores_case_and_surrounding_whitespace(self):
        self.assertEqual(
            cafeteria.find_special("  TUESDAY  "),
            ("Grilled Cheese Sandwich", 0.10),
        )

    def test_find_special_returns_none_for_days_without_special(self):
        self.assertEqual(cafeteria.find_special("Sunday"), (None, 0.0))

    def test_discounted_price_applies_discount_and_rounds_to_cents(self):
        self.assertEqual(cafeteria.discounted_price(4.25, 0.10), 3.83)
        self.assertEqual(cafeteria.discounted_price(1.00, 0.333), 0.67)

    def test_main_prints_special_price_and_discount_type(self):
        output = io.StringIO()

        with patch("builtins.input", return_value="Tuesday"):
            with redirect_stdout(output):
                cafeteria.main()

        printed = output.getvalue()
        self.assertIn("Today's special: Grilled Cheese Sandwich", printed)
        self.assertIn("Was $4.25, now $3.83", printed)
        self.assertIn("Discount value: 0.1", printed)
        self.assertIn("Discount type: <class 'float'>", printed)

    def test_main_reports_no_special_for_unmatched_day(self):
        output = io.StringIO()

        with patch("builtins.input", return_value="Sunday"):
            with redirect_stdout(output):
                cafeteria.main()

        self.assertIn("No special today.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
