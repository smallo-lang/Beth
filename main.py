import sys

import util
import loader
from prep import Preprocessor
from vm import VM

if __name__ == '__main__':
    if len(sys.argv) < 2:
        util.err('source file not specified')

    src = sys.argv[1]
    code = loader.load(src)
    pre = Preprocessor()
    pre.process(code)

    if pre.err:
        util.err('preprocessing error (try checking for duplicate labels)')

    VM(pre.instructions, pre.labels).boot()
