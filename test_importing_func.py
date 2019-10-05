from pathlib import Path
import check
import regex

folder_path = check.path_check(Path.home()/"programming/data/chrono24/")
file_iterator = check.gen_check(folder_path.rglob('*.jpg'),100)

for file in file_iterator:
    regex.replace_name(file.stem, '_', '+')