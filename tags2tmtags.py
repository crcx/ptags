#!/usr/bin/env python

def get_tags():
    with open('tags', 'r') as f:
        return f.readlines()


if __name__ == '__main__':
    tags = get_tags()
    for tag in tags:
        t = tag.strip().split('\t')
        name = t[0]
        file = t[1]
        line = t[2]
        tmtag = name + '\t' + file + '\t' + '/^\'' + name + '\'$/"\tfunction\tline:' + line + '\n'
        print tmtag
