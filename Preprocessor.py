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
        if label_id in self.labels:
            self.err = 'duplicate labels detected'
        else:
            self.labels[label_id] = len(self.instructions)

    def _check_no_instructions(self):
        if not self.instructions:
            self.err = 'instructions list is empty'

    @staticmethod
    def _is_label(line):
        return line[-1] == ':'

    @staticmethod
    def _parse_label_identifier(line):
        return line[:-1]
