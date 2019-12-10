import re
import itertools
import sys
from pathlib import Path

# TODO: Add commnets for each line in the main part of the program

def replace_path(path, pattern, replace):
    """Return the pathlib Path object obtained by replacing occurrences of 'pattern' in string by the 'replace'.
    """
    current_path = path.resolve()
    current_name = str(current_path.name)
    regex_pattern = re.compile(pattern, re.I)
    new_name = regex_pattern.sub(replace, current_name)
    new_path = current_path.with_name(new_name.lower())
    if current_path is not new_path:
        #print(f"{current_path} -> {new_path}")
        return current_path.replace(new_path)

def replace_name(name, pattern, replace):
    """Return the string obtained by replacing occurrences of 'pattern' in string by the 'replace'.
    """
    current_name = str(name)
    regex_pattern = re.compile(pattern, re.I)
    new_name = regex_pattern.sub(replace, current_name)
    if current_name is not new_name:
        print(f"{current_name} -> {new_name}")
        return new_name

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
    folder_path = Path.home()/'programming/data/chrono24/'
    file_iterator = gen_check(folder_path.rglob('*'))

    for count, file in enumerate(file_iterator):
        print(count)
        if count > 10:
            break
        #replace_path(file, r'\s', '_')
        #rm_version = replace_name(file.stem, r'(\s|-|\.)?(\d+$)', '')
        #words = r'(brand|new|mint|unworn|neue|bnib|nib|rare|box|papers|b&p|&gt|bracelet|strap|leather|rubber|silicone|oem|excellent|condition|and|or|with)?(\s|-|\+|,|:|;|"|\\|/)?'
        #rm_words = replace_name(rm_version, words, '')
        #rm_underscore = replace_name(rm_words, '_+', ' ')
    