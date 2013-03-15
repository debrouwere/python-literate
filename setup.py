import os
from setuptools import setup, find_packages
from literate import VERSION


f = open(os.path.join(os.path.dirname(__file__), 'README'))
readme = f.read()
f.close()

setup(
    name='python-literate',
    version=".".join(map(str, VERSION)),
    description='A wedding of literate programming and IPython notebooks. Create Markdown/HTML notebooks that include documentation, code and the output of that code.',
    long_description=readme,
    author='Stijn Debrouwere',
    author_email='stijn@stdout.be',
    url='http://github.com/stdbrouw/python-literate/tree/master',
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)

