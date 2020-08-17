from unittest import TestCase
import os

from Loader import Loader


class LoaderTest(TestCase):
    def setUp(self) -> None:
        self.loader = Loader('test.so')

    def tearDown(self) -> None:
        os.remove('test.so')

    def test_cleans_lines_around_clean_line(self):
        self._write_to_test_file('\t\nini n\n   \n')
        self.loader.load()
        self._assert_code_equals(['ini n'])

    def test_can_clean_comment(self):
        self._write_to_test_file('\t\nini n @ comment\n   \n')
        self.loader.load()
        self._assert_code_equals(['ini n'])

    """ Utility methods. """
    @staticmethod
    def _write_to_test_file(string):
        with open('test.so', 'w') as file:
            file.write(string)

    def _assert_code_equals(self, expect):
        self.assertEqual(expect, self.loader.code)
