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

    @property
    def html(self):
        return md.markdown(self.markdown)

    @property
    def markdown(self):
        if self.kind == 'markdown':
            return self.text.format(**self.variables)
        else:
            code = pad(self.text, '    ')
            output = pad(br(self.parse()), '> ')
            return "\n\n".join([code, output])

    def __repr__(self):
        return "<{kind} [{lines}]>".format(kind=self.kind, lines=len(self.raw))


def untangle(string, run=False):
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


def markdown(string, run=False):
    chunks = [chunk.markdown for chunk in untangle(string, run)]
    return u"\n\n".join(chunks)

def html(string, run=False):
    chunks = [chunk.html for chunk in untangle(string)]
    return u"\n\n".join(chunks)

def python(string, run=False):
    chunks = untangle(string)
    code = u"\n\n".join([chunk.text for chunk in chunks if chunk.kind is 'python'])
    if run:
        exec code
    else:
        return code