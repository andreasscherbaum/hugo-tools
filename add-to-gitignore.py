#!/usr/bin/env python3

import sys
import os

def add_file(filepath):
    if not (filepath.endswith('.jpg') or
            filepath.endswith('.jpeg') or
            filepath.endswith('.png') or
            filepath.endswith('.xcf')):
        return
    
    if not os.path.isfile(filepath):
        print("Not a file!")
        print(filepath)
        return
    
    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    
    gitignore_path = os.path.join(directory, '.gitignore')
    
    existing_lines = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as gitignore_file:
            existing_lines = gitignore_file.readlines()
    
    # check if the filename is already in .gitignore
    if filename + '\n' not in existing_lines:
        with open(gitignore_path, 'a') as gitignore_file:
            gitignore_file.write(filename + '\n')
        print(f"Added '{filename}' to {gitignore_path}")
    else:
        print(f"'{filename}' is already in {gitignore_path}")



def main():
    for filepath in sys.argv[1:]:
        add_file(filepath)

if __name__ == "__main__":
    main()
