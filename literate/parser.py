# encoding: utf-8

import sys
from cStringIO import StringIO
import markdown as md
import re


def br(string):
    # in Markdown, ending a line with more than one space
    # signifies a (single) line break
    return re.sub('\n{1}', '   \n', string)

def pad(string, padding):
    pattern = re.compile(r'^', re.MULTILINE)
    return re.sub(pattern, padding, string)


class Chunk(object):
    def __init__(self, kind, raw, variables={}):
        self.kind = kind
        self.raw = [raw]
        self.variables = variables

    def parse(self):
        if hasattr(self, '_parsed'):
            return self._parsed

        if self.kind == 'markdown':
            self._parsed = md.markdown(self.text)
        elif self.kind == 'python':
            stdout = sys.stdout
            sys.stdout = StringIO()
            exec self.text
            output = sys.stdout.getvalue()
            sys.stdout = stdout
            self.variables.update(locals())
            self._parsed = output
        else:
            raise ValueError()

        return self._parsed

    def append(self, line):
        self.raw.append(line)

    @property
    def lines(self):
        if self.kind == 'python':
            return [re.sub('^( {4}|\t)', '', line) for line in self.raw]
        else:
            return self.raw

    @property
    def text(self):
        return "\n".join(self.lines)

    def html(self, run):
        return md.markdown(self.markdown(run))

    def markdown(self, run):
        if self.kind == 'markdown':
            if run:
                return self.text.format(**self.variables)
            else:
                return self.text
        else:
            code = pad(self.text, '    ')
            if run:
                output = pad(br(self.parse()), '> ')
                return "\n\n".join([code, output])
            else:
                return code

    def __repr__(self):
        return "<{kind} [{lines}]>".format(kind=self.kind, lines=len(self.raw))


def untangle_docstrings(string, run=False):
    superchunks = string.strip().split('"""')
    chunks = []

    for i, superchunk in enumerate(superchunks):
        pass

    raise NotImplementedError()


def untangle_literate(string, run=False):
    lines = string.strip().split('\n')
    chunks = []

    for i, line in enumerate(lines):
        if line.startswith('\t') or line.startswith('    '):
            kind = 'python'
        else:
            kind = 'markdown'

        if len(chunks):
            same_kind = chunks[-1].kind is kind
            whitespace = len(lines[i].strip()) is 0 and not len(lines[i-1].strip()) is 0

            if same_kind or whitespace:
                chunks[-1].append(line)
            else:
                chunks.append(Chunk(kind, line))
        else:
            chunks.append(Chunk(kind, line))

    if run:
        # pre-parse our chunks, and give them the combined 
        # state of all previously parsed chunks too
        variables = {}
        for chunk in chunks:
            chunk.variables.update(variables)
            chunk.parse()
            variables.update(chunk.variables)

    return chunks


def untangle(string, run=False):
    return untangle_literate(string, run)


def pair(chunks):
    """
    Return matched pairs of (python, markdown) chunks, creating empty chunks 
    if necessary.
    
    This is useful for two-column layouts with documentation on the left and 
    code on the right.

    (Python on the left hand of the pair so we can parse the chunks in-order
    and have the Python state available to the accompanying documentation.)
    """
    raise NotImplementedError()


def markdown(string, run=False):
    chunks = [chunk.markdown(run) for chunk in untangle(string, run)]
    return u"\n\n".join(chunks)

def html(string, run=False):
    chunks = [chunk.html(run) for chunk in untangle(string, run)]
    return u"\n\n".join(chunks)

def python(string, run=False):
    chunks = untangle(string, run)
    code = u"\n\n".join([chunk.text for chunk in chunks if chunk.kind is 'python'])
    if run:
        exec code
    else:
        return code