#!/usr/bin/env python3

# -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# generate a ctags compatible tags file for parable
#
# constraints:
#
# - code can be in either a *.p or *.md file
#    - in *.p, everything is code
#    - in *.md, code either has four spaces at the start of the line or
#      is fenced with four backticks (````)
# - syntax for naming a function is ... complicated
#    - basic form:
#      [ ... ] 'name' :
#    - alternate form:
#      'name' [ ... ] .
#    - variable forms:
#      'name' var
#
#      ... 'name' var!
#
#      [ 'name' 'name2' 'name3' ... ] ::
#    - functions can span multiple source lines:
#      'hello' [ "-s" \
#          'hello world!' ] .
# - tag file formats
#   - classic ctags (for vim):
#      tag  filename  line#
#   - textmate requires:
#      tag  filename  /^search_string$/;"  function  line:line#
#   - replace the separators with a single tab

import fnmatch
import os


def get_tags_for(pat, textmate=False):
    tags = []
    matches = []
    for root, dir, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, pat):
            matches.append(os.path.join(root, filename))
    for f in matches:
        print('Scanning ' + f + '...')
        s = open(f, 'r').readlines()
        i = 1
        for l in s:
            if l.endswith('\' :\n'): tags.append((l, f, i))
            if l.strip().startswith('\'') and l.endswith(' .\n'): tags.append((l, f, i))
            i = i + 1
    return tags


def write_tags(tagfile, textmate=False):
    tags = get_tags_for('*.p')
    for l in sorted(tags):
        print(l)


if __name__ == '__main__':
    write_tags('tags')
