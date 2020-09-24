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
        self.vm.instructions = [
            'div 126 3 magic',
            'div magic 2 other',
        ]
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

    def test_gth_(self):
        self.vm.instructions = [
            'gth 1 2 false',
            'gth 2 1 true',
            'put 42 a',
            'put 42 b',
            'gth a b f',
        ]
        self.vm.tick()
        self._assert_name_equals(0, 'false')
        self.vm.tick()
        self._assert_name_equals(1, 'true')
        for i in range(3):
            self.vm.tick()
        self._assert_name_equals(0, 'f')

    def test_lth_(self):
        self.vm.instructions = [
            'lth 1 2 true',
            'lth 2 1 false',
            'put 42 a',
            'put 42 b',
            'lth a b f',
        ]
        self.vm.tick()
        self._assert_name_equals(1, 'true')
        self.vm.tick()
        self._assert_name_equals(0, 'false')
        for i in range(3):
            self.vm.tick()
        self._assert_name_equals(0, 'f')

    def test_geq_(self):
        self.vm.instructions = [
            'geq 1 2 false',
            'geq 2 1 true',
            'put 42 a',
            'put 42 b',
            'geq a b t',
        ]
        self.vm.tick()
        self._assert_name_equals(0, 'false')
        self.vm.tick()
        self._assert_name_equals(1, 'true')
        for i in range(3):
            self.vm.tick()
        self._assert_name_equals(1, 't')

    def test_leq_(self):
        self.vm.instructions = [
            'leq 1 2 true',
            'leq 2 1 false',
            'put 42 a',
            'put 42 b',
            'leq a b t',
        ]
        self.vm.tick()
        self._assert_name_equals(1, 'true')
        self.vm.tick()
        self._assert_name_equals(0, 'false')
        for i in range(3):
            self.vm.tick()
        self._assert_name_equals(1, 't')

    def test_eq_(self):
        self.vm.instructions = [
            'eq 1 1 true',
            'eq 1 2 false',
            'put "hi" a',
            'put "bye" b',
            'eq a b f',
        ]
        self.vm.tick()
        self._assert_name_equals(1, 'true')
        self.vm.tick()
        self._assert_name_equals(0, 'false')
        for i in range(3):
            self.vm.tick()
        self._assert_name_equals(0, 'f')

    def test_neq_(self):
        self.vm.instructions = [
            'neq 1 1 false',
            'neq 1 2 true',
            'put "hi" a',
            'put "bye" b',
            'neq a b t',
        ]
        self.vm.tick()
        self._assert_name_equals(0, 'false')
        self.vm.tick()
        self._assert_name_equals(1, 'true')
        for i in range(3):
            self.vm.tick()
        self._assert_name_equals(1, 't')

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
            self.assertEqual('hello world', output)

    def test_outl_(self):
        self.vm.instructions = ['outl "hello world"']
        with capture(self.vm.tick) as output:
            self.assertEqual('hello world\n', output)

    def test_nl_(self):
        self.vm.instructions = ['nl']
        with capture(self.vm.tick) as output:
            self.assertEqual('\n', output)

    def test_con_(self):
        self.vm.instructions = [
            'put 42 age',
            'con "hello " "world" msg',
            'con "I am " age msg',
        ]
        self.vm.tick()
        self.vm.tick()
        self._assert_name_equals('hello world', 'msg')
        self.vm.tick()
        self._assert_name_equals('I am 42', 'msg')

    def test_sti_(self):
        self.vm.instructions = [
            'put "42" magic',
            'sti "5" five',
            'sti magic magic',
            'sti "wrong" wrong'
        ]
        for i in range(4):
            self.vm.tick()
        self._assert_name_equals(5, 'five')
        self._assert_name_equals(42, 'magic')
        self._assert_err_flag_set()

    def test_not_(self):
        self.vm.instructions = [
            'put 0 i',
            'not 0 a',
            'not 1 b',
            'not "" c',
            'not "true" d',
            'not i e',
        ]
        for i in range(6):
            self.vm.tick()
        for name in ['a', 'c', 'e']:
            self._assert_name_true(name)
        for name in ['b', 'd']:
            self._assert_name_false(name)

    def test_and_(self):
        self.vm.instructions = [
            'put 0 a',
            'put 1 b',
            'and 1 1 true',
            'and a b false',
        ]
        for i in range(4):
            self.vm.tick()
        self._assert_name_true('true')
        self._assert_name_false('false')

    def test_or_(self):
        self.vm.instructions = [
            'put 0 a',
            'put 0 b',
            'or 1 0 true',
            'or a b false',
        ]
        for i in range(4):
            self.vm.tick()
        self._assert_name_true('true')
        self._assert_name_false('false')

    def test_jump_(self):
        self.vm.instructions = [
            'put 0 a',
            'jump point',
            'put 1 a',
            'end',
        ]
        self.vm.names = {'point': 3}
        for i in range(3):
            self.vm.tick()
        self._assert_name_equals(0, 'a')

    def test_jmpt_(self):
        self.vm.instructions = [
            'put 0 i',
            'jmpt i exit',  # no jump!
            'put 42 a',     # should be set to 42
            'put 1 i',
            'jmpt i exit',  # jump!
            'put 0 b',      # unreachable
        ]
        self.vm.names = {'exit': 6}
        for i in range(5):
            self.vm.tick()
        self._assert_name_equals(42, 'a')
        self.assertTrue('b' not in self.vm.names)

    def test_jmpf_(self):
        self.vm.instructions = [
            'put 1 i',
            'jmpf i exit',  # no jump!
            'put 42 a',     # should be set to 42
            'put 0 i',
            'jmpf i exit',  # jump!
            'put 0 b',      # unreachable
        ]
        self.vm.names = {'exit': 6}
        for i in range(5):
            self.vm.tick()
        self._assert_name_equals(42, 'a')
        self.assertTrue('b' not in self.vm.names)

    def test_br_(self):
        self.vm.instructions = [
            'put 0 i',
            'add i 1 i',
            'br start',
        ]
        self.vm.names = {'start': 1}
        self.vm.tick()      # i = 0
        for i in range(3):
            self._assert_name_equals(i, 'i')
            self.vm.tick()  # i += 1
            self.vm.tick()  # jump start
        self.assertEqual(3, self.vm.call.peek())

    def test_brt_(self):
        self.vm.instructions = [
            'put 0 i',
            'brt i exit',   # no jump!
            'put 42 a',     # should be set to 42
            'put 1 i',
            'brt i exit',   # jump!
            'put 0 b',      # unreachable
        ]
        self.vm.names = {'exit': 6}
        for i in range(5):
            self.vm.tick()
        self._assert_name_equals(42, 'a')
        self.assertTrue('b' not in self.vm.names)
        self.assertEqual(5, self.vm.call.peek())

    def test_brf_(self):
        self.vm.instructions = [
            'put 1 i',
            'brf i exit',   # no jump!
            'put 42 a',     # should be set to 42
            'put 0 i',
            'brf i exit',   # jump!
            'put 0 b',      # unreachable
        ]
        self.vm.names = {'exit': 6}
        for i in range(5):
            self.vm.tick()
        self._assert_name_equals(42, 'a')
        self.assertTrue('b' not in self.vm.names)
        self.assertEqual(5, self.vm.call.peek())

    def test_back_(self):
        self.vm.instructions = [
            'br make',
            'put 1 a',
            'end',
            'put "hi" b',
            'back',
        ]
        self.vm.names = {'make': 3}
        for i in range(4):
            self.vm.tick()
        self._assert_name_true('a')
        self._assert_name_equals("hi", 'b')

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

    """ Destructive tests. """
    def test_ini_responds_to_invalid_literal(self):
        self.vm.instructions = ['ini a']
        with mock.patch('builtins.input', return_value='wrong'):
            self.vm.tick()
        self._assert_err_flag_set()

    def test_sti_responds_to_invalid_literal(self):
        self.vm.instructions = ['sti "wrong" a']
        self.vm.tick()
        self._assert_err_flag_set()

    """ Utility methods. """
    def _assert_err_flag_set(self):
        self.assertTrue(self.vm.err)

    def _assert_name_equals(self, value, name):
        self.assertEqual(value, self.vm.names[name])

    def _assert_name_true(self, name):
        self._assert_name_equals(1, name)

    def _assert_name_false(self, name):
        self._assert_name_equals(0, name)
