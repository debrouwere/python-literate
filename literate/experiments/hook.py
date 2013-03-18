"""
The way in which a hijack / hook / override / patch 
works will be different for every class or library: 
sometimes it's a function, sometimes a class method, 
sometimes an instance method, but the mechanism is 
identical in all cases: take an object, return a 
modified or different one.

This way we can hook into the output of all sorts of 
different libraries and finetune the representation
for our python-literate reports, without having 
to change anything to those libraries themselves.
Add in images, HTML visualizations, tables and what-not.

See `load.py` for proof of concept.
"""

import pandas as pd

def hijack(cls):
    class Sub(cls):
        def plot(self, *vargs, **kwargs):
            return 'hijack!'
    return Sub

hijacks = []

def clshijack(cls):
    _plot = cls.plot
    def plot(*vargs, **kwargs):
        res = _plot(*vargs, **kwargs)
        hijacks.append(res)
        return res

    cls.plot = plot
    return cls

pd.Series = clshijack(pd.Series)