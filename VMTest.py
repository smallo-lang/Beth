from unittest import TestCase

from VM import VM


class VMTest(TestCase):
    def setUp(self) -> None:
        self.vm = VM()

    def test_decode_good_instruction(self):
        self.vm.instructions = ['put 1 a', 'end']
        self.vm.fetch()
        self.vm.decode()
        self.assertEqual('put', self.vm.opcode)
        self.assertEqual((1., 'a'), self.vm.operand)

    def test_decode_sets_err_flag_on_unknown_instruction(self):
        self.vm.instructions = ['unknown 1 a', 'end']
        self.vm.tick()
        self.assertTrue(self.vm.err)
        self.assertTrue(self.vm.exit_code)

    def test_decode_sets_err_flag_on_invalid_operand_length(self):
        self.vm.instructions = ['put 1', 'end']
        self.vm.tick()
        self.assertTrue(self.vm.err)
        self.assertTrue(self.vm.exit_code)

    """ Instruction set methods tests follow. """
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
