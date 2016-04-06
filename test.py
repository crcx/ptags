#!/usr/bin/env python3

import fnmatch
import os

def is_form1(l):
    flag = False
    if l.endswith('\' :\n'):
        flag = True
    return flag

def is_form2(l):
    flag = False
    if l.strip().startswith('\'') and l.endswith(' .\n'):
        flag = True
    return flag

def is_form3(l):
    flag = False
    if l.strip().startswith('\'') and l.endswith(' var\n'):
        flag = True
    if l.strip().startswith('\'') and l.endswith(' var!\n'):
        flag = True
    return flag

def is_form4(l):
    flag = False
    if l.strip().startswith('[ \'') and l.endswith(' ::\n'):
        flag = True
    return flag


def extract_tags(l, form):
    tags = []
    tokens = l.strip().split(' ')
    if form == 1 or form == 3:
        token = tokens[-2:][0:1][0]
        tags.append(token[1:-1])
        pass
    elif form == 2:
        pass
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
        print('Scanning ' + f + '...')
        s = open(f, 'r').readlines()
        i = 1
        for l in s:
            if is_form1(l):
                tags.append((1, extract_tags(l, 1), i, f))
            if is_form2(l):
                tags.append((2, l, i, f))
            if is_form3(l):
                tags.append((3, extract_tags(l, 3), i, f))
            if is_form4(l):
                tags.append((4, extract_tags(l, 4), i, f))
            i = i + 1
    return tags


def write_tags(tagfile, textmate=False):
    tags = get_tags_for('*.p')
    for l in sorted(tags):
        print(l)


if __name__ == '__main__':
    write_tags('tags')
