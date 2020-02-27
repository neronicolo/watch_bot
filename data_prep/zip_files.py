import argparse
import zipfile
from pathlib import Path

# creating ArgumentParser object 
parse = argparse.ArgumentParser(description='Recursively compress files from given directory to a single zip archive.')
# adding positional arguments
parse.add_argument('src_path', nargs='?', default=Path.cwd(), help='directory path, if omitted cdw() will be used')

source_path = Path.home()/'programming/data/watch_bot/zip_files_test/104'
source_name = 'test.txt'

dest_path = Path('/mnt/c/Users/neron/Downloads/')
dest_name = 'zip_test.zip'

with zipfile.ZipFile(dest_path/dest_name, 'w') as z:
    for file in source_path.rglob('*'):
        z.write(file)
