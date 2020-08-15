def _read_lines(src):
    with open(src) as file:
        return file.readlines()


def _clean_line(line):
    return line.split('@')[0].strip()


def _clean_lines(lines):
    clean_lines = []

    for line in lines:
        clean_line = _clean_line(line)
        if len(clean_line) > 0:
            clean_lines.append(clean_line)

    return clean_lines


def load(src):
    lines = _read_lines(src)
    return _clean_lines(lines)
