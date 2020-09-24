import sys

import util
from Loader import Loader
from Preprocessor import Preprocessor
from VM import VM

if __name__ == '__main__':
    if len(sys.argv) < 2:
        util.err('source file not specified')

    try:
        src = sys.argv[1]
        ldr = Loader()
        ldr.load(src)

        if ldr.err:
            util.err(f'[loader] {ldr.err}')

        pre = Preprocessor()
        pre.process(ldr.code)

        if pre.err:
            util.err(f'[preprocessor] {pre.err}')

        VM(pre.instructions, pre.labels).boot()
        
    except KeyboardInterrupt:
        util.keyboard_interrupt()
