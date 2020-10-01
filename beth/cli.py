import click
import colorama

from . import util
from .Loader import Loader
from .Preprocessor import Preprocessor
from .VM import VM

colorama.init()


@click.command(help='Run SmallO code.')
@click.argument(
    'source',
    type=click.Path(exists=True,
                    file_okay=True,
                    dir_okay=False),
)
def run(source):
    if util.source_file_extension_is_invalid(source):
        util.err("source file extension is invalid: '.so' expected")

    try:
        loader = Loader()
        loader.load(source)

        if loader.err:
            util.err(f'[loader] {loader.err}')

        pre = Preprocessor()
        pre.process(loader.code)

        if pre.err:
            util.err(f'[preprocessor] {pre.err}')

        VM(pre.instructions, pre.labels).boot()

    except KeyboardInterrupt:
        util.keyboard_interrupt()
