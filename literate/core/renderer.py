import jinja2
import utils

loader = jinja2.FileSystemLoader(utils.here('templates'))
environment = jinja2.Environment(loader=loader)

def passthrough():
    raise NotImplementedError()

def content(blocks):
    template = environment.get_template('content.html')
    return template.render(blocks=blocks)

def document(title, blocks, toc=None):
    template = environment.get_template('document.html')
    return template.render(title=title, blocks=blocks, toc=toc)