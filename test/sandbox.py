import literate
from pprint import pprint
import sys

ex = open('examples/basic/example.pylit').read()

def untangle():
    return literate.parser.untangle(ex)

def weave():
    blocks = literate.parser.weave(ex, simplify=True)
    print literate.renderer.content(blocks)

def package():
    literate.renderer.package('examples/basic', 'examples/basic/build')

ret = globals()[sys.argv[1]]()
if ret:
    pprint(ret)