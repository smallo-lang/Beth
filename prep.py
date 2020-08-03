import util


class Preprocessor:
    def __init__(self):
        self.instructions = []
        self.labels = {}
        self.err = False

    def process(self, code):
        for line in code:
            if self.err:
                break

            if self._is_label(line):
                self._check_and_add_label(line)
            else:
                self.instructions.append(line)

    def _check_and_add_label(self, line):
        label_id = self._parse_label_identifier(line)
        if label_id in self.labels:
            self.err = True
        else:
            self.labels[label_id] = len(self.instructions)

    @staticmethod
    def _is_label(line):
        return line[-1] == ':'

    @staticmethod
    def _parse_label_identifier(line):
        return line[:-1]
