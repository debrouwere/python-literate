#!/usr/bin/env python
# encoding: utf-8


import os
import shutil
import argparse
import parser
import loader


# patch the `import` statement so it can handle literate python
loader.patch()


def find(location):
    if os.path.isfile(location):
        return [location]
    elif os.path.isdir(location):
        ls = []
        for root, dirs, files in os.walk('./'):
            ls.extend([os.path.join(root, file) for file in files])
        return [file for file in ls if os.path.splitext(file)[1] in loader.EXTENSIONS]
    else:
        raise ValueError("Need a directory or a file.")

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


def out(output, dest, stdout):
    if stdout:
        print output
    else:
        try:
            os.makedirs(os.path.dirname(dest))
        except OSError:
            pass

        with open(dest, 'w') as f:
            f.write(output)


# TODO: all of this stuff should be in a submodule!

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

        if 'py' in options.formats:
            output = parser.python(src, run=False)
            out(output, dest + '.py', options.stdout)

        if 'md' in options.formats:
            output = parser.markdown(src, run=options.capture)
            out(output, dest + '.md', options.stdout)


def run(path):
    f = open(path).read()
    parser.python(f, run=True)


"""
TODO: figure out a better name than "untangle"
while it describes the process, it doesn't describe 
the fact that the Markdown and HTML files are rendered
results, not just a part of the original .pylit we 
extracted. `render` comes closer, but also not quite.
`run` doesn't have the connotation of generating output

noweb has `notangle` (produce code) and `noweave` (produce documentation)
(so you can do notangle myliterate.py | xargs python)
Sweave similarly has tangle and weave commands.

`unweave` perhaps has a more physical connotation than `untangle`.
Or perhaps it's really "untangling" (the code) but "weaving together" (a report).

If `untangle` produced any Markdown, to be consistent with the metaphor
it should give you the raw thing, either without any code (.md.py) or with the code unrun (.pylit)

And if we want to give `literate` the option to run your code through Python, 
maybe don't have a subcommand but just 

    literate code.pylit

or perhaps (if having it all as subcommands is more elegant)

    literate python code.pylit

and

    literate weave code.pylit --formats md html

and I don't think we really need a command that does both at the same time.
"""
def command():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    cli_run = subparsers.add_parser('run')
    cli_run.set_defaults(func=run, help='run a Literate Python script')
    cli_run.add_argument('src', nargs=1)
    cli_untangle = subparsers.add_parser('untangle', help='create HTML notebooks or an intermediate Markdown representation out of Literate Python scripts')
    cli_untangle.set_defaults(func=untangle)
    cli_untangle.add_argument('src', default='./', nargs='?', help='source file or directory')
    cli_untangle.add_argument('dest', default=None, nargs='?', help='destination file or directory')
    cli_untangle.add_argument('-t', '--template', default='./template', help='pass a custom HTML template')
    cli_untangle.add_argument('-f', '--formats', default=['md', 'py', 'html'], nargs='*', help="what formats you'd like to output")
    cli_untangle.add_argument('-p', '--print', dest='stdout', default=False, action='store_true', help="print to stdout (only useful when you've selected a single output format)")    
    cli_untangle.add_argument('-c', '--capture', default=False, action='store_true', help="run Python code and capture the output")    
    cli_untangle.add_argument('-r', '--recursive', default=False, action='store_true', help="look for .pylit files in any subdirectory") 
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    command()