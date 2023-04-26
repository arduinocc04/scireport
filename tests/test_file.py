import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src import file

def compare_files_ignoring_space(file1, file2):
    f = open(file1, 'r')
    g = open(file2, 'r')
    f_all = "".join([i.replace(" ","").replace("\n", "") for i in f.readlines()])
    g_all = "".join([i.replace(" ","").replace("\n", "") for i in g.readlines()])
    if len(f_all) != len(g_all):
        return False
    return f_all == g_all

class TestFileMethod(unittest.TestCase):
    def test_change_line_method(self):
        self.assertEqual(file.change_line("@@1.234 + 2.1@@", "@@"), "3.3")
        self.assertEqual(file.change_line("@@1.234 + !2.1@@", "@@"), "3.334")
        self.assertEqual(file.change_line("@@1.234_{1} + !2.1@@", "@@"), "3")
        self.assertEqual(file.change_line("@@!-1.234_{1} + 2.1@@", "@@"), "1.1")
    def test_change_file_method(self):
        inputName = "tests/data/test.tex"
        outputName = "tests/data/test_calced.tex"
        ideal = "tests/data/test_ideal.tex"
        file.change_file(inputName, outputName, "@@")
        self.assertTrue(compare_files_ignoring_space(outputName, ideal))

if __name__ == "__main__":
    unittest.main()