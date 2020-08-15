from unittest import TestCase

from Parser import Parser


class ParserTest(TestCase):
    def test_can_parse_instruction_with_no_operand(self):
        self._parse_and_check_result('end', 'end', ())

    def test_can_parse_instruction_with_one_label_operand(self):
        self._parse_and_check_result('jump start', 'jump', ('start',))

    def test_can_parse_instruction_with_one_int_operand(self):
        self._parse_and_check_result('put 1', 'put', (1,))

    def test_can_parse_instruction_with_one_str_operand(self):
        self._parse_and_check_result(
            'put "I love SmallO"', 'put', ('I love SmallO',))

    def test_can_parse_complex_instruction(self):
        self._parse_and_check_result(
            'add "one" 2 var', 'add', ('one', 2, 'var',))

    def _parse_and_check_result(self, instruction, opcode, operand):
        self.parser = Parser(instruction)
        self.parser.parse()
        self.assertEqual(opcode, self.parser.opcode)
        self.assertEqual(operand, self.parser.operand)
