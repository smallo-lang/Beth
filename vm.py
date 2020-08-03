import sys

from stack import Stack
import util
import loader
from preprocessor import Preprocessor


class VM:
    def __init__(self):
        self.ip = 0
        self.instruction = ''
        self.opcode = ''
        self.operand = ()
        
        self.labels = {}
        self.instructions = []
        self.variables = []
        self.returns = Stack()
        #   'opc': (fn pointer, operand length)
        self.opcodes = {
            'end': (self._end_, 0),
        }

    def boot(self, src):
        code = loader.load(src)
        self.labels, self.instructions = Preprocessor().preprocess(code)
        self._run()

    def _run(self):
        while True:
            self._tick()

    def _tick(self):
        self._fetch()
        self._decode()
        self._exec()

    def _fetch(self):
        self.instruction = self.instructions[self.ip]

    def _decode(self):
        self._parse()
        self._validate()

    def _parse(self):
        self.opcode = self.instruction  # temp
        self.operand = ()               # temp

    def _validate(self):
        if self.opcode not in self.opcodes:
            self._invalidate('unknown instruction', 1)
        
        expected_operand_length = self.opcodes[self.opcode][1]
        if len(self.operand) != expected_operand_length:
            self._invalidate('incorrect operand length', 1)

    def _invalidate(self, error_message, exit_code):
        self.opcode = 'err'
        self.operand = (error_message, exit_code)

    def _exec(self):
        opcode_method = self.opcodes[self.opcode][0]
        opcode_method(self.operand)

    # instruction set
    def _err_(self, operand):
        error_message, exit_code = operand
        print(f'Error: {error_message}')
        sys.exit(exit_code)

    def _end_(self, operand):
        sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        util.err('source file not specified')

    src = sys.argv[1]
    VM().boot(src)
