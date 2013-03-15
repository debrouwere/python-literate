./literate examples/basic/example.pylit examples/basic/tpl.html > examples/basic/example.html

Literate is a tiny tool that allows you to create prose documents interweaved with code, and 
display the output of that code alongside documentation and code itself.

Write your document in Markdown, and within the document, simply indent your code with four spaces or a tab.

Literate can also execute the code within your documents and capture the output, which 
is great for research notebooks, and akin to IPython notebooks, R Markdown, Sweave and Pweave.

Process both .pylit and .py.md (literate python) and .md.py (python with docstrings)

Allow people to specify whether they want to include output
(notebook mode) or not (regular literate programming), and whether to include code 
or just run it and make its state available for as variables (documentation mode)

literate run <file>                execute
literate untangle <file/folder>    output to .py and .md
    --template                     also output to HTML, using a template HTML file
    --formats                      any combination of py,md,html

Somewhat hackish at the moment, but it does work.

If you do `import literate` in your code, it'll import .pylit files like regular Python files.
(Warning: it usually does this by creating .pyc files with the same name as your literate
python file, but if you have a .py file with the same name as your .pyc file, it'll 
override that file as well. Don't create independent myproj.pylit and myproj.py files!)

Intersplice the markdown into a template (if specified on the CLI): replace <article/>

Variables can be used in the markdown, using the familiar {var} syntax you know from Python
string formatting.

Otherwise just output to .md and .py, which people can then use however they want (e.g. in Jekyll)

Dependencies: markdown

TODO
----

TODO: finish up the CLI.

Literate Python should also work with docstrings in regular Python files if that's more your cup of tea.
(I suppose the catch is that the one works with Python out of the box, the other works with Markdown
out of the box...)

TODO: inlining matplotlib figures would be nice too -- perhaps an extensible architecture that 
makes it easy to 'special-case' certain buffered output (and not just convert to __repr__); 
ideally we'd want something like this for d3 plots as well

TODO: make a really nice Hector template (routes, css, js, html) that works well with 
our .md output, and explain how you can go from pylit --> md --> documentation site 
(ideally you'd have these as steps in your Drakefile, BPipe, Fabric, whatever)

It's not `literate`'s job to provide a full html rendering framework. That's why so many 
documentation generators are a mess.