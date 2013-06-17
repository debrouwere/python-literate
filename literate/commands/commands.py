import fs
from literate import parser, templates, package

def run(options):
    for path in options.src:
        source = fs.File(path).read()
        parser.run(source)

def untangle(options):
    raise NotImplementedError()

def weave(options):
    src = fs.File(options.src)
    dest = fs.Directory(options.dest)

    # find literate python files
    if src.is_file:
        documents = [src]
    else:
        # TODO: specify whether we should search recursively or not
        # recursive=options.recursive
        # TODO: support for Literate Python with docstrings
        documents = fs.Directory(src.path).find('*.pylit') # '*.py.md', '.md.py'

    package.create(dest)

    # weave literate python
    for doc in documents:
        raw = doc.read()
        blocks = parser.weave(raw, evaluate=options.evaluate)
        # template=None
        # TODO: template should be handled differently depending on whether
        # it's a Jinja template (.html) or an executable that we should 
        # pass the context (w/ simplify=True above)
        html = templates.document(doc.name, blocks, prose=options.prose, capture=options.capture)
        filename = doc.name + '.html'
        f = fs.File(dest.path, filename)
        f.write(html)

    # documents are groups of blocks
    #literate.package(documents, options.dest)