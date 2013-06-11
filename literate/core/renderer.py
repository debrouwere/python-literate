import jinja2
import utils
import parser

loader = jinja2.FileSystemLoader(utils.here('templates'))
environment = jinja2.Environment(loader=loader)

def content(blocks):
    template = environment.get_template('content.html')
    return template.render(blocks=blocks)

def document(title, blocks, toc=None):
    template = environment.get_template('document.html')
    return template.render(title=title, blocks=blocks, toc=toc)

def pipe():
    raise NotImplementedError()

# REFACTOR: old code, but I want to offer similar functionality
# to provide a very easy way to allow for custom templating
def replace(src, body):
    assets = None

    if os.path.isfile(src):
        template = open(src).read()
    else:
        template = open(os.path.join(src, 'template.html')).read()
        assets_dir = os.path.join(src, 'assets')

        if os.path.exists(assets_dir):
            assets = assets_dir
    
    output = template.replace('<article/>', body)

    return (output, assets)