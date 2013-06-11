# encoding: utf-8

import __builtin__
import os
from tempfile import NamedTemporaryFile
import py_compile
import parser
from contextlib import contextmanager

builtin_import = __builtin__.__import__
EXTENSIONS = ('.py.md', '.pylit', )


@contextmanager
def tempfile(data):
    temp = NamedTemporaryFile(delete=False)
    temp.write(data)
    temp.close()
    yield temp.name
    os.unlink(temp.name)


def exists(name):
    for extension in EXTENSIONS:
        path = name.replace('.', '/') + extension
        if os.path.exists(path) is True:
            return (name, path)
    return False


def importer(name, globals=globals(), locals=locals(), fromlist=[], level=-1):
    try:
        return builtin_import(name, globals, locals, fromlist, level)
    except ImportError as error:
        location = exists(name)
        if location:
            name, path = location
            source = open(path).read()
            code = parser.python(source)
            dest = name + '.py'
            cache_dest = name + '.pyc'

            # the importer doesn't create plain `.py` files by itself, but 
            # the pylit executable can (if asked) and if they're there, we 
            # keep them up to date
            if os.path.exists(dest):
                with open(dest, 'w'):
                    dest.write(code)
            else:
                with tempfile(code) as buff:
                    py_compile.compile(buff, cache_dest, path, doraise=True)

            return builtin_import(name)
        else:
            raise error


def patch():
    __builtin__.__import__ = importer