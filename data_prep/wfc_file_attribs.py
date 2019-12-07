import check
import pandas as pd
from pathlib import Path
from PIL import Image
import collections
from tqdm import tqdm

# TODO: Sort files
# TODO: Do we need list if we have sorted infront of the generator:
#   https://docs.python.org/3/library/pathlib.html#pathlib.Path.rglob
#   file_list = sorted(dir_path.rglob('*.jpg'))
# TODO: make cli version of this program:
#   file_attrib(source folder(starting folder for recursion), csv_path(where to save), **kwargs(column for labelin))

dir_path = Path.home()/'programming/data/watch_bot/'
file_list = list(dir_path.rglob('*.jpg'))
file_list_sorted = sorted(set(file_list))
file_attribs = collections.defaultdict(list)

for file in tqdm(file_list_sorted[:20]):
    try:
        with Image.open(file) as img:
            image_size_x, image_size_y = img.size
            file_attribs['image_size_x'].append(image_size_x)
            file_attribs['image_size_y'].append(image_size_y)
    except OSError:
        continue
    file_attribs['name'].append(file.relative_to(dir_path))

# Crate DataFrame
df = pd.DataFrame.from_dict(file_attribs)
shape_init = df.shape

# Remove rows where image_size_x and image_size_y are less than the 'size'
size = 300
df = df[(df['image_size_x'] > size) & (df['image_size_y'] > size)]

# Adding labelling columns 
df['watch_face_visibility'] = -1
df['composition_quality'] = -1
df['light_quality'] = -1
df['image_quality'] = -1

print(f'initial dataframe shape: {shape_init}, new dataframe shape: {df.shape}')
print(file_list[:1], file_list_sorted[:1])
#df.to_csv(dir_path/'wfc_file_attribs.csv', index=False)
