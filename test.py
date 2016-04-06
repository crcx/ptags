#!/usr/bin/env python3

import fnmatch
import os


# form 0: not a definition
# form 1: [ ... ] 'name' :
# form 2: 'name' [ ... ] .
# form 3: 'name' var   OR   'name' var!
# form 4: [ 'name' 'name' ] ::

def determine_form(src):
    form = 0
    line = src.strip()
    if line.endswith('\' :'): form = 1
    if line.startswith('\'') and line.endswith(' .'): form = 2
    if line.startswith('\'') and line.endswith(' var'): form = 3
    if line.startswith('\'') and line.endswith(' var!'): form = 3
    if line.startswith('[ \'') and line.endswith(' ::'): form = 4
    return form


def extract_tags(src, form):
    tags = []
    tokens = src.strip().split(' ')
    if form == 1 or form == 3:
        token = tokens[-2:][0:1][0]
        tags.append(token[1:-1])
    elif form == 2:
        token = tokens[0:1][0]
        tags.append(token[1:-1])
    elif form == 4:
        token = tokens[1:-2]
        for t in token:
            if t != '':
                tags.append(t[1:-1])
    return tags


def get_tags_for(pat, textmate=False):
    tags = []
    matches = []
    for root, dir, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, pat):
            matches.append(os.path.join(root, filename))
    for f in matches:
        words = []
        print('Scanning ' + f + '...')
        s = open(f, 'r').readlines()
        i = 1
        for l in s:
            form = determine_form(l)
            if form != 0:
                for tag in extract_tags(l, form):
                    words.append((tag, f, i))
            i = i + 1
        print(' + ' + str(len(words)) + ' identified')
        tags = tags + words
    return sorted(tags)


def write_tags(tagfile, textmate=False):
    tags = get_tags_for('*.p')
    for l in tags:
        print(l)


if __name__ == '__main__':
    write_tags('tags')
