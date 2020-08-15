from unittest import TestCase

from Preprocessor import Preprocessor


class PreprocessorTest(TestCase):
    def setUp(self) -> None:
        self.pre = Preprocessor()

    def test_sets_err_flag_on_empty_code(self):
        self.pre.process([])
        self.assertTrue(self.pre.err)

    def test_works_for_one_instruction_code(self):
        self.pre.process(['inn n'])
        self.assertEqual(['inn n'], self.pre.instructions)
        self.assertEqual({}, self.pre.labels)

    def test_works_for_label_and_instruction(self):
        self.pre.process(['start:', 'inn n'])
        self.assertEqual(['inn n'], self.pre.instructions)
        self.assertEqual({'start': 0}, self.pre.labels)

    def test_sets_err_flag_on_duplicate_labels(self):
        self.pre.process(['start:', 'end', 'start:', 'add 1 2 s', 'back'])
        self.assertTrue(self.pre.err)

    def test_works_for_good_code(self):
        self.pre.process([
            'inn age',
            'lth age 18 b',
            'jmpf b exit',
            'out "You are a minor"',
            'exit:',
            'end',
        ])
        self.assertEqual([
            'inn age',
            'lth age 18 b',
            'jmpf b exit',
            'out "You are a minor"',
            'end',
        ], self.pre.instructions)
        self.assertEqual({'exit': 4}, self.pre.labels)
        self.assertFalse(self.pre.err)
