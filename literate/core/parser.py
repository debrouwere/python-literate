# encoding: utf-8

import sys
import utils
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

def strip(l):
    while len(l) and not len(l[0]):
        l = l[1:]
    while len(l) and not len(l[-1]):
        l = l[:-1]
    return l

def issibling(a, b):
    return a.__class__ == b.__class__

class Chunk(object):
    def __init__(self, raw, variables={}):
        self.raw = [raw]
        self.variables = variables
        self.output = False

    def append(self, line):
        self.raw.append(line)

    @property
    def text(self):
        return "\n".join(self.lines)

    def html(self, run):
        return md.markdown(self.markdown(run))

    @property
    def name(self):
        return self.__class__.__name__.lower().replace('chunk', '')

    def __repr__(self):
        return "<{kind} [{lines}]>".format(kind=self.name, lines=len(self.lines))

    @property
    def is_empty(self):
        return not len(self.lines)


class PythonChunk(Chunk):
    def parse(self):
        if self.output is not False:
            return self.output

        stdout = sys.stdout
        sys.stdout = StringIO()
        exec self.text
        self.output = sys.stdout.getvalue()
        sys.stdout = stdout
        self.variables.update(locals())

        return self.output

    @property
    def lines(self):
        _lines = [re.sub('^( {4}|\t)', '', line) for line in self.raw]
        return strip(_lines)

    # THOUGHT: I think I want to leave it up to the templating layer 
    # to decide how to display the output. So we'll pass on chunks
    # w/ {type, raw, html, output}
    def markdown(self, run):
        code = pad(self.text, '    ')
        if run:
            output = pad(br(self.parse()), '> ')
            return "\n\n".join([code, output])
        else:
            return code

    # See note above.
    def serialize(self):
        return {
            'type': self.name, 
            'text': self.text,
            'html': False,
            'output': self.output,
        }

class MarkdownChunk(Chunk):
    def parse(self):
        if hasattr(self, '_parsed'):
            return self._parsed

        self._parsed = md.markdown(self.text)
        return self._parsed

    @property
    def lines(self):
        return strip(self.raw)

    # THOUGHT: I think I want to leave it up to the templating layer 
    # to decide how to display the output. So we'll pass on chunks
    # w/ {type, raw, html, output}
    def markdown(self, run=True):
        if run:
            try:
                return self.text.format(**self.variables)
            except KeyError, name:
                raise KeyError(utils.line("""
                    You referenced {name} in your literate document, 
                    but no such variable was found. Did you enable 
                    code evaluation?".format(name=name))
                    """, name=name))
        else:
            return self.text

    # See note above.
    def serialize(self):
        return {
            'type': self.name, 
            'raw': self.text, 
            'html': self.html(True), 
            'output': False, 
        }

class Document(object):
    def weave(self, evaluate=True, simplify=False):
        blocks = []
        variables = {}
        for chunk in self.chunks:
            if evaluate:
                # pre-parse our chunks, and give them the combined 
                # state of all previously parsed chunks too
                chunk.variables.update(variables)
                chunk.parse()
                variables.update(chunk.variables)

        pairs = []
        pair = {}
        for chunk in self.chunks:
            if simplify:
                data = chunk.serialize()
            else:
                data = chunk

            if isinstance(chunk, MarkdownChunk) and len(pair):
                pairs.append(pair)
                pair = {}

            if isinstance(chunk, MarkdownChunk):
                pair.setdefault('prose', []).append(data)
            else:
                pair.setdefault('code', []).append(data)

            prev = chunk

        pairs.append(pair)
        return pairs

    def untangle(self):
        types = {'python': '', 'markdown': ''}

        for chunk in self.chunks:
            types[chunk.name] += chunk.text + '\n'

        return types

    def run(self):
        code = self.untangle()['python']
        exec code

    def __init__(self, raw):
        self.raw = raw
        self.tokenize()


class LiterateDocument(Document):
    def categorize(self, line):
        if line.startswith('\t') or line.startswith('    '):
            return PythonChunk
        else:
            return MarkdownChunk       

    def tokenize(self):
        lines = self.raw.strip().split('\n')
        chunks = []

        for i, line in enumerate(lines):
            Chunk = self.categorize(line)

            if len(chunks):
                prev = lines[i-1].strip()
                cur = lines[i].strip()
                same_kind = isinstance(chunks[-1], Chunk)
                whitespace = len(cur) is 0 and not len(prev) is 0
                double_space = len(cur) is 0 and len(prev) is 0
                same_kind = same_kind or whitespace
                continuation = same_kind and not double_space
            else:
                continuation = False

            if continuation:
                chunks[-1].append(line)
            else:
                chunks.append(Chunk(line))

        self.chunks = filter(lambda chunk: not chunk.is_empty, chunks)

    def untangle(self, pure=False):
        types = super(LiterateDocument, self).untangle()
        # pure means what we remove any python code from our markdown
        # document (this is usually not what you want)
        if not pure:
            types['markdown'] = self.raw

        return types

class DocStringDocument(Document):
    def untangle(self, pure=False):
        types = super(DocStringDocument, self).untangle()
        # pure means what we remove any docstrings from our python
        # code (this is usually not what you want)
        if not pure:
            types['python'] = self.raw

        return types

def weave(string, evaluate=True, simplify=True):
    document = LiterateDocument(string)
    return document.weave(evaluate=evaluate, simplify=simplify)

def untangle(string):
    document = LiterateDocument(string)
    return document.untangle()

def run(string):
    document = LiterateDocument(string)
    document.run()