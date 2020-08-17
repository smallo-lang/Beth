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

            'gth': (self._gth_, 3),
            'lth': (self._lth_, 3),
            'geq': (self._geq_, 3),
            'leq': (self._leq_, 3),

            'eq': (self._eq_, 3),
            'neq': (self._neq_, 3),

            'ini': (self._ini_, 1),
            'ins': (self._ins_, 1),
            'out': (self._out_, 1),

            'con': (self._con_, 3),
            'sti': (self._sti_, 2),

            'jump': (self._jump_, 1),
            'jmpt': (self._jmpt_, 2),
            'jmpf': (self._jmpf_, 2),
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
            self._invalidate(f'unknown opcode: {self.opcode}')
        
        _, expected_operand_length = self.opcodes[self.opcode]
        if len(self.operand) != expected_operand_length:
            self._invalidate(f'incorrect operand length: {self.instruction}')

    def _invalidate(self, error_message, exit_code=1):
        self.opcode = 'err'
        self.operand = (
            (State.STRING, error_message),
            (State.INTEGER, exit_code)
        )

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

    def _binary_value_unpack(self, operand):
        x, y, var = operand
        x = self._eval_value(x)
        y = self._eval_value(y)
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

    """ Binary integer arithmetic operations. """
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

    """ Binary integer comparisons. """
    def _gth_(self, operand):
        x, y, var = self._binary_integer_unpack(operand)
        self._store_name(var, int(x > y))

    def _lth_(self, operand):
        x, y, var = self._binary_integer_unpack(operand)
        self._store_name(var, int(x < y))

    def _geq_(self, operand):
        x, y, var = self._binary_integer_unpack(operand)
        self._store_name(var, int(x >= y))

    def _leq_(self, operand):
        x, y, var = self._binary_integer_unpack(operand)
        self._store_name(var, int(x <= y))

    """ Binary general exact comparisons. """
    def _eq_(self, operand):
        x, y, var = self._binary_value_unpack(operand)
        self._store_name(var, int(x == y))

    def _neq_(self, operand):
        x, y, var = self._binary_value_unpack(operand)
        self._store_name(var, int(x != y))

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

    """ String operations. """
    def _con_(self, operand):
        x, y, var = self._binary_value_unpack(operand)
        self._store_name(var, f'{x}{y}')

    def _sti_(self, operand):
        string, var = operand
        string = self._eval_string(string)
        var = self._eval_variable(var)
        try:
            self._store_name(var, int(string))
        except ValueError:
            self._invalidate('invalid literal for integer conversion')

    """ Control flow. """
    def _jump_(self, operand):
        location = self._eval_name(operand[0])
        self.ip = location

    def _jmpt_(self, operand):
        var, location = operand
        var = self._eval_name(var)
        location = self._eval_name(location)
        if var:
            self.ip = location

    def _jmpf_(self, operand):
        var, location = operand
        var = self._eval_name(var)
        location = self._eval_name(location)
        if not var:
            self.ip = location

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
