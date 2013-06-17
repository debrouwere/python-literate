import templates, utils, parser
import fs

def create(dest):
    if isinstance(dest, basestring):
        dest = fs.Directory(dest)

    # create or clear destination
    if dest.exists:
        dest.remove(recursive=True)
    dest.create()

    # copy over assets
    assets = fs.Directory(utils.here('../build/resources'))
    assets.copy(dest, root=True)
    vendor = fs.Directory(utils.here('../vendor'))
    vendor.copy(fs.Directory(dest.path, 'resources'), root=True)