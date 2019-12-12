#!/home/nikola/anaconda3/envs/python37/bin/python

###
# Nikola Dordic
# https://nidjo.com
# 28-Avg-2019
###

"""
    usage: unrar_recur.py [-h] [src_path] [dest_path]

    Recursively extracts files inside given folder.

    positional arguments:
      src_path    set source path, if not cwd() wiil be used
      dest_path   set destination path, if not cwd() wiil be used

    optional arguments:
      -h, --help  show this help message and exit
"""

from pathlib import Path
import rarfile
import argparse
import sys
import itertools
from tqdm import tqdm

# TODO: Add Exception if file can not be unrared. Test without and figure out what exception to use
# TODO: Combina zip and rar into one program
#   https://stackoverflow.com/questions/18653025/python-zip-extraction-exception
# TODO: Why it's not working on WSL

# creating ArgumentParser object
parser = argparse.ArgumentParser(description='Recursively extracts files inside given folder.')
# adding positional arguments
parser.add_argument('src_path', nargs='?', default=Path.cwd(), help='set source path, if not cwd() wiil be used')
parser.add_argument('dest_path', nargs='?', default=Path.cwd(), help='set destination path, if not cwd() wiil be used')
# parsing arguments
args = parser.parse_args()

# Add args to dict.
paths = {'src_path':args.src_path, 'dest_path':args.dest_path}

# Check whether paths exist or not.
for path in paths.keys():
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
        print('No RAR files found.')
        sys.exit(1)
    return itertools.chain([first], iterable)

# If extract_folder folder exist, increment it.
for file in files_found(paths['src_path'].rglob('*.rar')):
    print(f'File:{file}')
    counter = 1
    while True:
        extract_folder = paths['dest_path']/(file.stem + '_' + str(counter))
        if not extract_folder.exists():
            break
        counter += 1
    print(f'Extract to folder: {extract_folder}')

    # Convert pathlib objects to strings.
    file_str = str(file)
    extract_folder_str = str(extract_folder)

    # Extract rar archive to destination folder.
    with rarfile.RarFile(file_str) as rar_archive:
        try:
            rar_archive.extractall(extract_folder_str)
        except rarfile.Error:
            continue
        print("Done.")
