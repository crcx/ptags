# PTAGS

Tools to generate *ctags* compatible tag files for Parable code.

### Some notes

I've encountered two file formats.

Minimal tag file:

    tag filename line#

TextMate requires something more:

    tag filename /^'tag'$/;" function line:line#

In both of these, replace the spaces with tabs.

I prefer dealing with the original ctags format as it's very simple and direct.

Parable sources can either be plain source (*.p) or Markdown (*.md)

Functions get a form like:

    [ .... ] 'name' :

Or:

    'name' [ .... ] .

It's easier to catch the first form (the second may have the . on a separate line)
