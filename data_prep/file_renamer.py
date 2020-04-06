import re
import itertools
import sys
from pathlib import Path
from tqdm import tqdm

def remove_umlaut(string):
    """
    Removes umlauts from strings and replaces them with the letter+e convention
    :param string: string to remove umlauts from
    :return: unumlauted string
    """
    u = 'ü'.encode()
    U = 'Ü'.encode()
    a = 'ä'.encode()
    A = 'Ä'.encode()
    o = 'ö'.encode()
    O = 'Ö'.encode()
    ss = 'ß'.encode()

    string = string.encode()
    string = string.replace(u, b'ue')
    string = string.replace(U, b'Ue')
    string = string.replace(a, b'ae')
    string = string.replace(A, b'Ae')
    string = string.replace(o, b'oe')
    string = string.replace(O, b'Oe')
    string = string.replace(ss, b'ss')

    string = string.decode('utf-8')
    return string

def fix_unicode(string):
    string = string.encode('ascii', 'ignore').decode('ascii')
    return string

def replace_path(path, pattern, replace, replace_umlaut=True):
    """Return the pathlib Path object obtained by replacing occurrences of 'pattern' in string by the 'replace'. Converts path to lower key. Replaces umlaut by default."""
    current_path = path.resolve()
    current_name = str(current_path.name)
    regex_pattern = re.compile(pattern, re.I)
    new_name = regex_pattern.sub(replace, current_name)
    if replace_umlaut:
        new_name = remove_umlaut(new_name)
        new_name = fix_unicode(new_name)
    new_path = current_path.with_name(new_name.lower())
    # if path doesn't exist
    if not new_path.exists():
        #print(f"{current_path} -> {new_path}")  
        return current_path.replace(new_path)

def replace_name(name, pattern, replace):
    """Return the string obtained by replacing occurrences of 'pattern' in string by the 'replace'. Meant to be used on strings."""
    current_name = str(name)
    regex_pattern = re.compile(pattern, re.I)
    new_name = regex_pattern.sub(replace, current_name)
    if current_name is not new_name:
        #print(f"{current_name} -> {new_name}")
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
    imgs_dir_path = Path.home()/'programming/data/watch_bot/'
    file_list = imgs_dir_path.rglob('*')

    for file in tqdm(file_list):
        # replace "spaces" in path with "_" and also make everything lower key
        replace_path(file, r'\s', '_')
        
        # remove dashes from version 
        #rm_version = replace_name(file.stem, r'(\s|-|\.)?(\d+$)', '')

        # TODO: Add comments to the lines below
        #words = r'(brand|new|mint|unworn|neue|bnib|nib|rare|box|papers|b&p|&gt|bracelet|strap|leather|rubber|silicone|oem|excellent|condition|and|or|with)?(\s|-|\+|,|:|;|"|\\|/)?'
        #rm_words = replace_name(rm_version, words, '')
        #rm_underscore = replace_name(rm_words, '_+', ' ')