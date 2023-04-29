import typing
import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src import num

class TestNumMethods(unittest.TestCase):
    def test_significant_count_method(self):
        self.assertEqual(num.count_significant_figure("1.234"), 4)
        self.assertEqual(num.count_significant_figure("10000", strict=True), 1)
        self.assertEqual(num.count_significant_figure("10000", strict=False), 5)
        self.assertEqual(num.count_significant_figure("0.00001"), 1)
        self.assertEqual(num.count_significant_figure("10001"), 5)
        self.assertEqual(num.count_significant_figure("50000.", True), 5)

    def test_change_e_not_2_LaTeX_method(self):
        self.assertEqual(num.change_e_notation_2_LaTeX_notation("1e3"), "1\\times 10^{3}")
        self.assertEqual(num.change_e_notation_2_LaTeX_notation("-1e3"), "-1\\times 10^{3}")
        self.assertEqual(num.change_e_notation_2_LaTeX_notation("1e-3"), "1\\times 10^{-3}")
        self.assertEqual(num.change_e_notation_2_LaTeX_notation("-1e-3"), "-1\\times 10^{-3}")

    def test_arithmetic_method(self):
        self.assertEqual((num.SuperFloat("1.34634") + num.SuperFloat("24.22")).string, "25.57")
        self.assertEqual((num.SuperFloat("1.34134") + num.SuperFloat("24.22")).string, "25.56")
        self.assertEqual((num.SuperFloat("234234.3") * num.SuperFloat("1.111")).string, "260200")
        self.assertEqual((num.SuperFloat("-1") * num.SuperFloat("1")).string, "-1")

    def test_float_string_2_e_notation_method(self):
        self.assertEqual(num.change_float_string_2_e_notation("1.234"), "1.234")
        self.assertEqual(num.change_float_string_2_e_notation("-1.234"), "-1.234")
        self.assertEqual(num.change_float_string_2_e_notation("-12.34"), "-1.234e1")
        self.assertEqual(num.change_float_string_2_e_notation("12.34"), "1.234e1")
        self.assertEqual(num.change_float_string_2_e_notation("-0.1234"), "-1.234e-1")
        self.assertEqual(num.change_float_string_2_e_notation("0.1234"), "1.234e-1")


if __name__ == "__main__":
    unittest.main()