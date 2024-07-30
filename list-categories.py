#!/usr/bin/env python3

import os
import sys
import re
import pathlib
from pprint import pprint
import yaml

start = "content/post"
categories = []


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
        categories = yml['categories']
    except KeyError:
        print("No categories in file!")
        print(f"File: {full_filename}")
        sys.exit(1)

    return categories



for rootpath, dirs, files in os.walk(start):
    for filename in files:
        if (filename != "index.md"):
            continue
        this_categories = handle_file(rootpath, filename, os.path.join(rootpath, filename))
        if (None in this_categories):
            print("Stop here ...")
            print(this_categories)
            print(os.path.join(rootpath, filename))
            sys.exit(1)

        if (len(this_categories) > 0):
            categories.extend(this_categories)

categories = list(set(categories))

#print("\n".join(categories))
#sys.exit(1)

categories.sort()
if (len(sys.argv) > 1):
    search = sys.argv.copy()
    search.pop(0)
    for c in categories:
        found = 0
        for s in search:
            if (s in c):
                found += 1
            else:
                break
        if (found > 0 and found == len(search)):
            print(c)
else:
    # just print them all
    print("\n".join(categories))
