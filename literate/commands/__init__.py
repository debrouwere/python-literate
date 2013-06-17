import argparse
import commands

def initialize():
    arguments = argparse.ArgumentParser()
    subparsers = arguments.add_subparsers()

    run = subparsers.add_parser('run')
    run.set_defaults(func=commands.run, help="run a Literate Python script")
    run.add_argument('src', nargs=1)

    weave = subparsers.add_parser('weave', 
        help="create HTML notebooks or an intermediate Markdown representation \
            out of Literate Python scripts")
    weave.set_defaults(func=commands.weave)
    weave.add_argument('src', 
        default='./', nargs='?', 
        help="source file or directory")
    weave.add_argument('dest', 
        default='./notebook', nargs='?', 
        help="destination file or directory")
    weave.add_argument('-t', '--template', 
        help="pass woven files to an executable instead of the default templating engine")
    weave.add_argument('-r', '--recursive', 
        default=False, action='store_true', 
        help="look for .pylit files in subdirectories")
    weave.add_argument('-e', '--evaluate',
        default=False, action='store_true',
        help="evaluate the code and make global variables available to the prose")
    weave.add_argument('-c', '--capture',
        default=False, action='store_true',
        help="capture and display the code's output")
    weave.add_argument('-p', '--prose',
        default=False, action='store_true',
        help="display only prose, not code")

    untangle = subparsers.add_parser('untangle', 
        help="untangle code from documentation and write away both to separate files")
    untangle.set_defaults(func=commands.untangle)
    untangle.add_argument('-f', '--formats', 
        default=['md', 'py'], nargs='*', 
        help="what formats you'd like to output")
    untangle.add_argument('-p', '--print', 
        dest='stdout', default=False, action='store_true', 
        help="print to stdout (only useful when you've selected \
            a single output format)")    
    untangle.add_argument('-r', '--recursive', 
        default=False, action='store_true', 
        help="look for .pylit files in subdirectories")

    args = arguments.parse_args()
    args.func(args)