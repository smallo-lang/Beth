import re


class Preprocessor:
    def __init__(self):
        self.instructions = []
        self.labels = {}
        self.err = ''

    def process(self, code):
        for line in code:
            if self.err:
                break

            if self._is_label(line):
                self._check_and_add_label(line)
            else:
                self.instructions.append(line)

        self._check_no_instructions()

    def _check_and_add_label(self, line):
        label_id = self._parse_label_identifier(line)

        if not self._is_valid_label(line):
            self.err = f'label {line} is invalid'
        elif label_id in self.labels:
            self.err = f'duplicate labels detected: {line}'
        else:
            self.labels[label_id] = len(self.instructions)

    def _check_no_instructions(self):
        if not self.instructions:
            self.err = 'instructions list is empty'

    @staticmethod
    def _is_label(line):
        return line[-1] == ':'

    @staticmethod
    def _is_valid_label(line):
        return bool(re.search('[_a-zA-Z][_a-zA-Z0-9]*', line))

    @staticmethod
    def _parse_label_identifier(line):
        return line[:-1]
