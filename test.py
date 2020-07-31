import sys

import util
import vm

vm = vm.VM()
vm._preprocess(code=['end'])
vm._run()
