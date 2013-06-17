# encoding: utf-8

VERSION = (0, 0, 1)

from core import loader, parser, templates, package, utils
import commands

# patch the `import` statement so it can handle literate python
loader.patch()

if __name__ == '__main__':
    commands.initialize()