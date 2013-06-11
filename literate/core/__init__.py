def run(path):
    f = open(path).read()
    parser.python(f, run=True)