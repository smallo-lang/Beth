import sys

import util
import Loader
from Preprocessor import Preprocessor
from VM import VM

if __name__ == '__main__':
    if len(sys.argv) < 2:
        util.err('source file not specified')

    src = sys.argv[1]
    code = Loader.load(src)
    pre = Preprocessor()
    pre.process(code)

    if pre.err:
        util.err(f'preprocessing error: {pre.err}')

    VM(pre.instructions, pre.labels).boot()
