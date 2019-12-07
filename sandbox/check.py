from pathlib import Path
import itertools
import sys

def path_check(path):
    """Check if path exists. If True return path, if False raise FileNotFoundError."""
    try:
        Path(path).resolve(strict=True)
    except FileNotFoundError:
        print("Path doesn't exist.")
        sys.exit(1)
    else:
        return path

def gen_check(iterable, iter_limit=None):
    """Check if generator is empty. If True raise StopIteration, if False return iterator until iteration limit is met."""
    try:
        first_item = next(iterable)
    except StopIteration:
        print("No files found")
        sys.exit(1)
    else:
        next_element = itertools.chain([first_item], iterable)
        return itertools.islice(next_element, iter_limit)

if __name__ == "__main__":
    folder_path = path_check(Path.home()/"programming/data/chrono24/Sinn_1")
    file_iterator = gen_check(folder_path.rglob('*.jpg'),100)

    for file in file_iterator:
        print(file)

