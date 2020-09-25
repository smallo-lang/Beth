import sys

from Stack import Stack
from Parser import Parser, State


class VM:
    def __init__(self, instructions=[], labels={}):
        self.ip = 0
        self.instruction = ''
        self.opcode = ''
        self.operand = ()

        self.instructions = instructions + ['end']
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
            'outl': (self._outl_, 1),
            'nl': (self._nl_, 0),

            'con': (self._con_, 3),
            'sti': (self._sti_, 2),

            'not': (self._not_, 2),
            'and': (self._and_, 3),
            'or': (self._or_, 3),

            'jump': (self._jump_, 1),
            'jmpt': (self._jmpt_, 2),
            'jmpf': (self._jmpf_, 2),

            'br': (self._br_, 1),
            'brt': (self._brt_, 2),
            'brf': (self._brf_, 2),
            'back': (self._back_, 0),

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
        if self.err:
            return
        self.decode()
        if self.err:
            return
        self.exec()

    def fetch(self):
        if self.ip < 0 or self.ip >= len(self.instructions):
            self._error(f'instruction pointer out of bounds: {self.ip}')
            return

        self.instruction = self.instructions[self.ip]
        self.ip += 1

    def decode(self):
        self._parse()
        self._validate()

    def _parse(self):
        parser = Parser()
        parser.parse(self.instruction)
        self.opcode = parser.opcode
        self.operand = parser.operand

    def _validate(self):
        if self.opcode not in self.opcodes:
            self._error(f'unknown opcode: {self.opcode}')
            return
        
        _, expected_operand_length = self.opcodes[self.opcode]
        if len(self.operand) != expected_operand_length:
            self._error(f'incorrect operand length: {self.instruction}')

    def _error(self, error_message, exit_code=1):
        self.err = error_message
        self.exit_code = exit_code

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

    def _push_call(self):
        self.call.push(self.ip)

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
        string = ''
        try:
            string = input()
            self._store_name(var, int(string))
        except ValueError:
            self._error(
                f'invalid literal "{string}" for integer conversion')

    def _ins_(self, operand):
        var = self._eval_variable(operand[0])
        self._store_name(var, input())

    def _out_(self, operand):
        print(self._eval_value(operand[0]), end='')

    def _outl_(self, operand):
        print(self._eval_value(operand[0]))

    def _nl_(self, operand):
        print()

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
            self._error(
                f'invalid literal "{string}" for integer conversion')

    """ Boolean operations. """
    def _not_(self, operand):
        val, var = operand
        val = self._eval_value(val)
        var = self._eval_variable(var)
        self._store_name(var, int(not val))

    def _and_(self, operand):
        x, y, var = self._binary_value_unpack(operand)
        self._store_name(var, int(x and y))

    def _or_(self, operand):
        x, y, var = self._binary_value_unpack(operand)
        self._store_name(var, int(x or y))

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

    def _br_(self, operand):
        self._push_call()
        location = self._eval_name(operand[0])
        self.ip = location

    def _brt_(self, operand):
        var, location = operand
        var = self._eval_name(var)
        location = self._eval_name(location)
        if var:
            self._push_call()
            self.ip = location

    def _brf_(self, operand):
        var, location = operand
        var = self._eval_name(var)
        location = self._eval_name(location)
        if not var:
            self._push_call()
            self.ip = location

    def _back_(self, operand):
        if self.call.empty():
            self._error(
                'attempt to branch back with empty call stack at ' +
                f'instruction {self.ip}'
            )
        else:
            self.ip = self.call.pop()

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
