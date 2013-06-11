import os
import shutil

def weave(options):
    locations = find(options.src)
    template = options.template

    for location in locations:
        src = open(location).read()

        if options.dest:
            base = options.dest
            basename = os.path.splitext(os.path.basename(location))[0]
            dest = os.path.join(base, basename)
        else:
            dest = os.path.splitext(location)[0]
            base = os.path.dirname(dest)

        if 'html' in options.formats:
            body = parser.html(src, run=options.capture)
            body = "<article>{}</article>".format(body)
            template = render(options.template, body)
            output = template[0].replace('<article/>', body)

            out(output, dest + '.html', options.stdout)

            if template[1]:
                assets_dest = os.path.join(base, os.path.basename(template[1]))
                if os.path.exists(assets_dest):
                    shutil.rmtree(assets_dest)
                shutil.copytree(template[1], assets_dest)

def render(src, body):
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