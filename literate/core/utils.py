import os
import shutil
import re
from copy import copy

def line(string, **kwargs):
    string = string.format(**kwargs)
    string = re.sub(r'\n+', ' ', string)
    return re.sub(r'\s{2,}', ' ', string)

def here(*segments):
    current = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(current, '..', *segments))

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