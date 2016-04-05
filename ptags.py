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
#   - 

import argparse
import fnmatch
import os

def tag(tag, file, line, textmate):
    if textmate:
        return tag + '\t' + os.getcwd() + '/' + file[2:] + '\t' + '/^\'' + tag + '\'$/;"\tfunction\tline:' + str(line)
    else:
        return tag + '\t' + os.getcwd() + '/' + file[2:] + '\t' + str(line)

def tag_for_colon(l, f, i, textmate):
    t = l.split(' ')
    print('  ' + t[-2:-1][0][1:-1])
    return tag(t[-2:-1][0][1:-1], f, i, textmate)


def tag_for_dot(l, f, i, textmate):
     t = l.strip().split(' ')
     print('  ' + t[0:1][0][1:-1])
     return tag(t[0:1][0][1:-1], f, i, textmate)


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
            if l.endswith('\' :\n'): tags.append(tag_for_colon(l, f, i, textmate))
            if l.strip().startswith('\'') and l.endswith(' .\n'): tags.append(tag_for_dot(l, f, i, textmate))
            i = i + 1
    return tags


def write_tags(tagfile, textmate=False)
    with open(tagfile, 'w') as f:
        tags = get_tags_for('*.p')
        tags = tags + get_tags_for('*.md')
        for l in sorted(tags):
            f.write(l + '\n')
    return len(tags)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ctags for parable')
    parser.add_argument('--ctags', help='generate vim compatible tags', action="store_true")
    parser.add_argument('--tmtags', help='generate textmate compatible tags', action="store_true")
    args = vars(parser.parse_args())

    if args['ctags']:
        write_tags('tags')

    if args['tmtags']:
        write_tags('tmtags', textmate=True)

    if not args['ctags'] and not args['tmtags']:
        print('Specify tags format!')
