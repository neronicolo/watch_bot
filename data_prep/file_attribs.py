import sys
from pathlib import Path
import check
import  regex
import pandas as pd
import collections
from PIL import Image
import time

start_time = time.time()

def convert_bytes(byte_size):
    """Converts bytes to human readable file size. Returns size in human readable units."""
    size_units = {0:'B', 1:'KB', 2:'MB', 3:'GB', 4:'TB'}
    # 2**10 = 1024
    power = 2**10
    counter = 0
    while byte_size > power:
        byte_size /= power
        counter += 1 
    return round(byte_size, 1), size_units[counter]

directory_path = check.path_check(Path.home()/"programming/data/chrono24/")
file_iterator = check.gen_check(directory_path.rglob('*.jpg'))
file_attribs = collections.defaultdict(list)

# TODO: add progress bar https://tqdm.github.io
# TODO: Check which attributes(colums) we need to create 
# TODO: Test if is an image, is needed? import imghdr vs PIL. fastClass cwegner git
# TODO: Check if watch model is in watch name if so return match
# TODO: Clean up watch name from ad related wording
# TODO: Move logic to def main()? if __name__ == "__main__":
# TODO: Do I need sorted?

for file in sorted(file_iterator):
    try:
        file_attribs['image_size'].append(Image.open(file).size)
    except OSError:
        continue
    file_attribs['file_path'].append(file)
    file_attribs['file_name'].append(file.name)
    file_attribs['file_extension'].append(file.suffix)
    file_attribs['file_size'].append(convert_bytes(file.stat().st_size))
    file_attribs['watch_brand'].append(file.parent.parts[-2])
    file_attribs['watch_model'].append(file.parent.parts[-1])
    file_attribs['watch_name'].append(str(file.stem.split('-')[:-1]).replace('_',' '))

# Create pandas DataFrame
df = pd.DataFrame.from_dict(file_attribs)
#print(df.iloc[:, 2].head(50))

# Write to DataFrame to csv
#df.to_csv('sinn_file_attribs.csv', index=False)

print(f"{time.time() - start_time} seconds")