import pandas as pd
from pathlib import Path
from PIL import Image
import collections
from tqdm import tqdm

# TODO: make cli version of this program:
#   file_attrib(source folder(starting folder for recursion), csv_path(where to save), **kwargs(column for labelin))

# save csv to
csv_file_path = Path.home()/'programming/projects/watch_bot/data_prep/wfc_file_attribs.csv'
# directory path where images are stored
imgs_dir_path = Path.home()/'programming/data/watch_bot/'

file_list = sorted(imgs_dir_path.rglob('*.jpg'))
file_attribs = collections.defaultdict(list)

for file in tqdm(file_list):
    try:
        with Image.open(file) as img:
            image_size_x, image_size_y = img.size
            file_attribs['image_size_x'].append(image_size_x)
            file_attribs['image_size_y'].append(image_size_y)
    except OSError:
        continue
    file_attribs['name'].append(file.relative_to(imgs_dir_path))

# Crate DataFrame
df = pd.DataFrame.from_dict(file_attribs)
shape_init = df.shape

# Remove rows where image_size_x and image_size_y are less than the 'size'
size = 300
df = df[(df['image_size_x'] > size) & (df['image_size_y'] > size)]

# Adding labelling columns 
df['dial_visibility'] = -1
df['like'] = -1 
df['image_quality'] = -1

print(f'initial dataframe shape: {shape_init}, new dataframe shape: {df.shape}')
df.to_csv(csv_file_path, index=False)
