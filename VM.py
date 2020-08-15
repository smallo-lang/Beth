import sys

from stack import Stack
import util
import Loader
from Preprocessor import Preprocessor
from Parser import Parser


class VM:
    def __init__(self, instructions=[], labels={}):
        self.ip = 0
        self.instruction = ''
        self.opcode = ''
        self.operand = ()

        self.instructions = instructions
        self.labels = labels
        self.variables = {}
        self.call = Stack()

        self.run = True
        self.err = ''
        self.exit_code = 0

        #   'opc': (fn pointer, operand length)
        self.opcodes = {
            'put': (self._put_, 2),
            'err': (self._err_, 2),
            'end': (self._end_, 0),
        }

    def boot(self):
        while self.run and not self.err:
            self.tick()

        if self.err:
            print(f'Error: {self.err}')

        sys.exit(self.exit_code)

    def tick(self):
        self.fetch()
        self.decode()
        self.exec()

    def fetch(self):
        self.instruction = self.instructions[self.ip]

    def decode(self):
        self._parse()
        self._validate()

    def _parse(self):
        parser = Parser(self.instruction)
        parser.parse()
        self.opcode = parser.opcode
        self.operand = parser.operand

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
    def _put_(self, operand):
        val, var = operand
        self.variables[var] = val

    def _err_(self, operand):
        self.err, self.exit_code = operand

    def _end_(self, operand):
        self.run = False
