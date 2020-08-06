import sys

from stack import Stack
import util
import loader
from prep import Preprocessor


class VM:
    def __init__(self, instructions, labels):
        self.ip = 0
        self.instruction = ''
        self.opcode = ''
        self.operand = ()

        self.instructions = instructions
        self.labels = labels
        self.variables = {}
        self.call = Stack()
        #   'opc': (fn pointer, operand length)
        self.opcodes = {
            'err': (self._err_, 2),
            'end': (self._end_, 0),
        }

    def boot(self):
        while True:
            self.fetch()
            self.decode()
            self.exec()

    def fetch(self):
        self.instruction = self.instructions[self.ip]

    def decode(self):
        self._parse()
        self._validate()

    def _parse(self):
        self.opcode = self.instruction  # temp
        self.operand = ()               # temp

    def _validate(self):
        if self.opcode not in self.opcodes:
            self._invalidate('unknown opcode', 1)
        
        _, expected_operand_length = self.opcodes[self.opcode]
        if len(self.operand) != expected_operand_length:
            self._invalidate('incorrect operand length', 1)

    def _invalidate(self, error_message, exit_code):
        self.opcode = 'err'
        self.operand = (error_message, exit_code)

    def exec(self):
        opcode_method, _ = self.opcodes[self.opcode]
        opcode_method(self.operand)

    """ Instruction set methods follow. """
    def _err_(self, operand):
        error_message, exit_code = operand
        print(f'Error: {error_message}')
        sys.exit(exit_code)

    def _end_(self, operand):
        sys.exit(0)
