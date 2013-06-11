import renderer as render
import fs

def package(src, dest):
    src = fs.File(src)
    dest = fs.Directory(dest)

    # find literate python files
    if src.is_file:
        documents = [src]
    else:
        documents = fs.Directory(src.path).find('*.pylit')

    # create or clear destination
    if dest.exists:
        dest.remove(recursive=True)
    dest.create()

    # copy over assets
    assets = fs.Directory(utils.here('templates/assets'))
    assets.copy(dest, root=True)

    # weave literate python
    for doc in documents:
        raw = doc.read()
        blocks = parser.weave(raw)
        html = render.document(doc.name, blocks)
        filename = doc.name + '.html'
        f = fs.File(dest.path, filename)
        f.write(html)