from pathlib import Path
import itertools
import sys
import regex

def path_exists(path):
    """Checks if path exists. If True returns path, if False raises FileNotFoundError."""
    try:
        path.resolve(strict=True)
    except FileNotFoundError:
        print("Path doesn't exist.")
        sys.exit(1)
    else:
        return path

def file_exists(iterable, iter_limit=None):
    """Checks if generator is empty. If True raises StopIteration, if False returns iterator until iteration limit is met."""
    try:
        first_item = next(iterable)
    except StopIteration:
        print("No files found")
        sys.exit(1)
    else:
        next_element = itertools.chain([first_item], iterable)
        return itertools.islice(next_element, iter_limit)

folder_path = path_exists(Path("/home/neronicolo/programming/data/chrono24"))
file_iterator = file_exists(folder_path.rglob('*.jpg'),10)

for file in file_iterator:
    regex.replace_name(file.stem, '_', '+')