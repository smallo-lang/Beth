class Loader:
    def __init__(self, src):
        self.src = src
        self.code = []

    def load(self):
        return self._clean_lines()

    def _clean_lines(self):
        for line in self._read_lines():
            clean_line = self._clean_line(line)
            if clean_line:
                self.code.append(clean_line)

    def _read_lines(self):
        with open(self.src) as file:
            return file.readlines()

    @staticmethod
    def _clean_line(line):
        return line.split('@')[0].strip()
