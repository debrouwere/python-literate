import os

def untangle(options):
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
 
        if 'py' in options.formats:
            output = parser.python(src, run=False)
            out(output, dest + '.py', options.stdout)

        if 'md' in options.formats:
            output = parser.markdown(src, run=options.capture)
            out(output, dest + '.md', options.stdout)