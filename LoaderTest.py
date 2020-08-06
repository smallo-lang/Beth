from unittest import TestCase
import os

import loader


class LoaderTest(TestCase):
    def test_cleans_lines_around_clean_line(self):
        self._write_to_test_file('\t\ninn n\n   \n')
        clean_lines = self._load()
        self.assertEqual(['inn n'], clean_lines)

    def test_can_clean_comment(self):
        self._write_to_test_file('\t\ninn n @ comment\n   \n')
        clean_lines = self._load()
        self.assertEqual(['inn n'], clean_lines)

    def tearDown(self) -> None:
        os.remove('test.so')

    @staticmethod
    def _write_to_test_file(string):
        with open('test.so', 'w') as file:
            file.write(string)

    @staticmethod
    def _load():
        return loader.load('test.so')
