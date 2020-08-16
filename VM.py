import sys

from Stack import Stack
from Parser import Parser, State


class VM:
    def __init__(self, instructions=[], labels={}):
        self.ip = 0
        self.instruction = ''
        self.opcode = ''
        self.operand = ()

        self.instructions = instructions
        self.names = labels
        self.call = Stack()

        self.run = True
        self.err = ''
        self.exit_code = 0

        #   'opc': (fn pointer, operand length)
        self.opcodes = {
            'put': (self._put_, 2),
            'add': (self._add_, 3),
            'sub': (self._sub_, 3),
            'mul': (self._mul_, 3),
            'div': (self._div_, 3),
            'mod': (self._mod_, 3),

            'ini': (self._ini_, 1),
            'ins': (self._ins_, 1),
            'out': (self._out_, 1),

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
        self.ip += 1

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
            self._invalidate('unknown opcode')
        
        _, expected_operand_length = self.opcodes[self.opcode]
        if len(self.operand) != expected_operand_length:
            self._invalidate('incorrect operand length')

    def _invalidate(self, error_message, exit_code=1):
        self.opcode = 'err'
        self.operand = (error_message, exit_code)

    def exec(self):
        opcode_method, _ = self.opcodes[self.opcode]
        opcode_method(self.operand)

    def _eval_name(self, tok):
        kind, name = tok

        if kind != State.IDENTIFIER:
            return None

        try:
            return self.names[name]
        except KeyError:
            return None

    def _eval_integer(self, tok):
        kind, integer = tok

        if kind == State.STRING:
            return None
        elif kind == State.INTEGER:
            return integer
        else:
            return self._eval_name(tok)

    def _eval_string(self, tok):
        kind, string = tok

        if kind == State.STRING:
            return string
        elif kind == State.INTEGER:
            return None
        else:
            return self._eval_name(tok)

    def _eval_value(self, tok):
        kind, value = tok

        if kind == State.IDENTIFIER:
            return self._eval_name(tok)
        else:
            return value

    @staticmethod
    def _eval_variable(tok):
        return tok[1]

    def _binary_integer_unpack(self, operand):
        x, y, var = operand
        x = self._eval_integer(x)
        y = self._eval_integer(y)
        var = self._eval_variable(var)
        return x, y, var

    def _store_name(self, name, value):
        self.names[name] = value

    """ Instruction set methods follow. """

    """ Assignment. """
    def _put_(self, operand):
        val, var = operand
        val = self._eval_value(val)
        var = self._eval_variable(var)
        self._store_name(var, val)

    """ Binary integer operations. """
    def _add_(self, operand):
        x, y, var = self._binary_integer_unpack(operand)
        self._store_name(var, x + y)

    def _sub_(self, operand):
        x, y, var = self._binary_integer_unpack(operand)
        self._store_name(var, x - y)

    def _mul_(self, operand):
        x, y, var = self._binary_integer_unpack(operand)
        self._store_name(var, x * y)

    def _div_(self, operand):
        x, y, var = self._binary_integer_unpack(operand)
        self._store_name(var, x // y)

    def _mod_(self, operand):
        x, y, var = self._binary_integer_unpack(operand)
        self._store_name(var, x % y)

    """ I/O operations. """
    def _ini_(self, operand):
        var = self._eval_variable(operand[0])
        try:
            self._store_name(var, int(input('# ')))
        except ValueError:
            self._invalidate('invalid literal for integer conversion')

    def _ins_(self, operand):
        var = self._eval_variable(operand[0])
        self._store_name(var, input('$ '))

    def _out_(self, operand):
        print(self._eval_value(operand[0]))

    """ Control flow. """
    def _err_(self, operand):
        err, exit_code = operand
        self.err = self._eval_value(err)
        if self.err is None:
            self.err = ''

        self.exit_code = self._eval_integer(exit_code)
        if self.exit_code is None:
            self.exit_code = 0

    def _end_(self, operand):
        self.run = False
