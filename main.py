import sys

import util
from Loader import Loader
from Preprocessor import Preprocessor
from VM import VM

if __name__ == '__main__':
    if len(sys.argv) < 2:
        util.err('source file not specified')

    src = sys.argv[1]
    ldr = Loader(src)
    ldr.load()

    pre = Preprocessor()
    pre.process(ldr.code)

    if pre.err:
        util.err(f'preprocessing error: {pre.err}')

    VM(pre.instructions, pre.labels).boot()
