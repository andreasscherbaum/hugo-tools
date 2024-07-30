#!/usr/bin/env python3

import os
import sys
import re
import pathlib
from pprint import pprint
import yaml

start = "content/post"
tags = []


def split_file(data, filename):
    if (data[0:4] != "---\n"):
        print("Content does not start with Frontmatter!")
        print("File: {f}".format(f = filename))
        sys.exit(1)

    parts = re.search(r'^\-\-\-\n(.*?)\n\-\-\-\n(.*)$', data, re.DOTALL)
    if (not parts):
        print("Can't extract Frontmatter from data!")
        print("File: {f}".format(f = filename))
        sys.exit(1)

    frontmatter = parts.group(1).strip()
    body = parts.group(2).strip()

    return frontmatter, body


def handle_file(rootpath, filename, full_filename):
    with open(full_filename) as fh:
        data = fh.read()

    frontmatter, body = split_file(data, full_filename)

    yml = yaml.safe_load(frontmatter)
    try:
        tags = yml['tags']
    except KeyError:
        print("No tags in file!")
        print(f"File: {full_filename}")
        sys.exit(1)

    return tags



for rootpath, dirs, files in os.walk(start):
    for filename in files:
        if (filename != "index.md"):
            continue
        this_tags = handle_file(rootpath, filename, os.path.join(rootpath, filename))
        if (None in this_tags):
            print("Stop here ...")
            print(this_tags)
            print(os.path.join(rootpath, filename))
            sys.exit(1)

        if (len(this_tags) > 0):
            tags.extend(this_tags)

tags = list(set(tags))

#print("\n".join(tags))
#sys.exit(1)

tags.sort()
if (len(sys.argv) > 1):
    search = sys.argv.copy()
    search.pop(0)
    for t in tags:
        found = 0
        for s in search:
            if (s in t):
                found += 1
            else:
                break
        if (found > 0 and found == len(search)):
            print(t)
else:
    # just print them all
    print("\n".join(tags))
