#!/home/nikola/anaconda3/envs/python37/bin/python

###
# Nikola Dordic
# https://nidjo.com
# 28-Avg-2019
###

"""
    usage: unzip_recur.py [-h] [src_path] [dest_path]

    Recursively extracts files inside given folder.

    positional arguments:
      src_path    set source path, if not cwd() wiil be used
      dest_path   set destination path, if not cwd() wiil be used

    optional arguments:
      -h, --help  show this help message and exit
"""

import argparse
import itertools
import sys
import zipfile
from pathlib import Path

# creating ArgumentParser object
parser = argparse.ArgumentParser(description='Recursively extracts files from given directory.')
# adding positional arguments
parser.add_argument('src_path', nargs='?', default=Path.cwd(), help='source path, if omitted cdw() will be used')
parser.add_argument('dest_path', nargs='?', default=Path.cwd(), help='destination path, if omitted cdw() will be used')
# parsing arguments
args = parser.parse_args()

# Add args to dict.
paths = {'src_path':args.src_path, 'dest_path':args.dest_path}

# Check whether paths exist or not.
for path in paths:
    try:
        paths[path] = Path(paths[path]).resolve(strict=True)
        # If path is not a directory.
        if not paths[path].is_dir():
            print(f"Path '{paths[path]}' is not a directory.")
            sys.exit(1)
    except FileNotFoundError:
        print(f"Path '{paths[path]}' doesn't exist.")
        sys.exit(1)

# If path doesn't contain iterable generator returns None
def files_found(iterable):
    try:
        first = next(iterable)
    except StopIteration:
        print('No ZIP files found.')
        sys.exit(1)
    return itertools.chain([first], iterable)

# If extract_folder folder exist, increment it.
for file in files_found(paths['src_path'].rglob('*.zip')):
    print(f'File:{file}')
    counter = 1
    while True:
        extract_folder = paths['dest_path']/(file.stem + '_' + str(counter))
        if not extract_folder.exists():
            break
        counter += 1
    print(f'Extract to folder: {extract_folder}')

    # Extract zip archive to destination folder.
    with zipfile.ZipFile(file) as zip_archive:
        try:
            zip_archive.extractall(extract_folder)
        except zipfile.BadZipFile:
            continue
        print("Done.")
