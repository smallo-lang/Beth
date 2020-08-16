from unittest import TestCase, mock
import sys
from io import StringIO
from contextlib import contextmanager

from VM import VM


@contextmanager
def capture(command, *args, **kwargs):
    out, sys.stdout = sys.stdout, StringIO()
    try:
        command(*args, **kwargs)
        sys.stdout.seek(0)
        yield sys.stdout.read()
    finally:
        sys.stdout = out


class VMTest(TestCase):
    def setUp(self) -> None:
        self.vm = VM()

    def test_decode_sets_err_flag_on_unknown_instruction(self):
        self.vm.instructions = ['unknown 1 a']
        self.vm.fetch()
        self.vm.decode()
        self._assert_err_flag_set()

    def test_decode_sets_err_flag_on_invalid_operand_length(self):
        self.vm.instructions = ['put 1']
        self.vm.fetch()
        self.vm.decode()
        self._assert_err_flag_set()

    """ Instruction set methods tests follow. """
    def test_put_(self):
        self.vm.instructions = ['put 1 a', 'put a b']
        self.vm.tick()
        self._assert_name_equals(1, 'a')
        self.vm.tick()
        self._assert_name_equals(1, 'b')

    def test_add_(self):
        self.vm.instructions = ['add 40 2 magic', 'add magic 3 other']
        self.vm.tick()
        self._assert_name_equals(42, 'magic')
        self.vm.tick()
        self._assert_name_equals(45, 'other')

    def test_sub_(self):
        self.vm.instructions = ['sub 44 2 magic', 'sub magic 2 other']
        self.vm.tick()
        self._assert_name_equals(42, 'magic')
        self.vm.tick()
        self._assert_name_equals(40, 'other')

    def test_mul_(self):
        self.vm.instructions = ['mul 21 2 magic', 'mul magic 3 other']
        self.vm.tick()
        self._assert_name_equals(42, 'magic')
        self.vm.tick()
        self._assert_name_equals(126, 'other')

    def test_div_(self):
        self.vm.instructions = ['div 126 3 magic', 'div magic 2 other']
        self.vm.tick()
        self._assert_name_equals(42, 'magic')
        self.vm.tick()
        self._assert_name_equals(21, 'other')

    def test_mod_(self):
        self.vm.instructions = ['mod 42 40 magic', 'mod magic 2 other']
        self.vm.tick()
        self._assert_name_equals(2, 'magic')
        self.vm.tick()
        self._assert_name_equals(0, 'other')

    def test_ini_(self):
        self.vm.instructions = ['ini magic', 'ini wrong']
        with mock.patch('builtins.input', return_value='42'):
            self.vm.tick()
        self._assert_name_equals(42, 'magic')
        with mock.patch('builtins.input', return_value='wrong'):
            self.vm.tick()
        self._assert_err_flag_set()

    def test_ins_(self):
        self.vm.instructions = ['ins msg']
        with mock.patch('builtins.input', return_value='hello world'):
            self.vm.tick()
        self._assert_name_equals('hello world', 'msg')

    def test_out_(self):
        self.vm.instructions = ['out "hello world"']
        with capture(self.vm.tick) as output:
            self.assertEquals('hello world\n', output)

    def test_err_(self):
        self.vm.instructions = ['err "just an error message" 1']
        self.vm.tick()
        self.assertTrue(self.vm.run)
        self.assertEqual('just an error message', self.vm.err)
        self.assertTrue(self.vm.exit_code)

    def test_end_(self):
        self.vm.instructions = ['end']
        self.vm.tick()
        self.assertFalse(self.vm.run)
        self.assertFalse(self.vm.err)
        self.assertFalse(self.vm.exit_code)

    """ Utility methods. """
    def _assert_err_flag_set(self):
        self.assertEqual('err', self.vm.opcode)

    def _assert_name_equals(self, value, name):
        self.assertEqual(value, self.vm.names[name])
