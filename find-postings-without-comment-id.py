#!/usr/bin/env python3

# pylint: disable=invalid-name

"""
Find every blog posting (index.md) which is committed in git,
but is missing comments->id
For details see this posting:
https://andreas.scherbaum.la/post/2024-05-23_client-side-comments-with-mastodon-on-a-static-hugo-website/
"""

import os
import sys
import re
import subprocess
import yaml


def scan_directory(directory:str) -> list:
    """
    Recursively scans the directory for files named 'index.md'
    This only works if Hugo Bundles are used
    Otherwise the blog postings can be any .md file
    """

    index_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file == "index.md":
                index_files.append(os.path.join(root, file))

    index_files.sort(reverse = True)
    return index_files


# split_file_into_frontmatter_and_markdown()
#
# separate the Frontmatter header and the Markdown content
#
# parameter:
#  - copy of the file content
# return:
#  - frontmatter
#  - markdown
def split_file_into_frontmatter_and_markdown(data:str) -> list[str, str]:
    """
    separate the Frontmatter header and the Markdown content
    """

    if data[0:4] != "---\n":
        sys.exit(1)

    parts = re.search(r'^---\n(.*?)\n---\n(.*)$', data, re.DOTALL)
    if not parts:
        sys.exit(1)

    frontmatter = parts.group(1).strip()
    body = parts.group(2).strip()

    return frontmatter, body


# file_is_added_in_git()
#
# check if a file is added in git
#
# parameter:
#  - filename
# return:
#  - True: file is added
#  - False: file is not added, or not a git repository
def file_is_added_in_git(filename:str) -> bool:
    """
    check if a file is ignored in git
    """

    rc = False
    try:
        result = subprocess.run( # pylint: disable=W1510
            ['git', 'ls-files', '--error-unmatch', filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        return_code = result.returncode
        if return_code == 0: # pylint: disable=R1703
            # RC=0 is only set if the file is added in git
            rc = True
        else:
            # RC=1 is set when file is not added
            # RC=128 is set when this is not a git repository
            rc = False
        stdout = result.stdout.strip() # pylint: disable=W0612
        stderr = result.stderr.strip()
        if len(stderr) > 0:
            # something went wrong
            rc = False

    except Exception as e: # pylint: disable=W0718,W0612
        rc = False

    return rc


# handle_markdown_file()
#
# handle the checks for a single Markdown file
#
# parameter:
#  - filename of Markdown file
# return:
#  - 0/1 (0: ok, 1: something wrong or changed)
def handle_markdown_file(filename:str): # pylint: disable=R0912, R0915
    """
    handle the checks for a single Markdown file
    """

    with open(filename, encoding="utf-8") as fh:
        data = fh.read()

    frontmatter, _ = split_file_into_frontmatter_and_markdown(data)

    try:
        yml = yaml.safe_load(frontmatter)
    except yaml.YAMLError as e:
        print(f"Error parsing frontmatter in {filename}: {e}")
        sys.exit(1)
    if 'comments' not in yml:
        # nothing in Fromtmatter
        return

    comments = yml['comments']
    if comments is None:
        # it's empty
        return

    if 'id' in comments:
        if comments['id'] is None:
            print("Comments ID is not set!")
            print(filename)
            return
        if len(str(comments['id']).strip()) < 1:
            print("Comments ID is not set!")
            print(filename)
            return



def main():
    """
    main function
    """

    if len(sys.argv) < 2:
        print("Usage:")
        print("")
        print("  {sys.argv[0]} <directory> [<directory>, <director<>]")
        print("")
        sys.exit(1)

    directories = sys.argv[1:]
    failed = False

    for directory in directories:
        if not os.path.isdir(directory):
            print(f"Directory does not exist: {directory}")
            failed = True
    if failed:
        sys.exit(1)

    for directory in directories:
        index_files = scan_directory(directory)
        if index_files:
            #print(f"Found 'index.md' in the following locations within '{directory}':")
            for file in index_files:
                if file_is_added_in_git(file):
                    #print(file)
                    handle_markdown_file(file)


if __name__ == "__main__":
    main()
