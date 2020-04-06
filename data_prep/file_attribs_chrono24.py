import pandas as pd
from pathlib import Path
from PIL import Image
import collections
from tqdm import tqdm

# TODO: make cli version of this program:
#   file_attrib(source folder(starting folder for recursion), csv_path(where to save), **kwargs(column for labelin))

# directory path where images are stored
data_path = Path.home()/'programming/data/chrono24/'
# save csv to
csv_path = data_path/'file_attribs_chrono24.csv'

file_list = sorted(data_path.rglob('*.jpg'))
file_attribs = collections.defaultdict(list)

for file in tqdm(file_list):
    try:
        with Image.open(file) as img:
            image_size_x, image_size_y = img.size
            file_attribs['image_size_x'].append(image_size_x)
            file_attribs['image_size_y'].append(image_size_y)
    except OSError:
        continue
    file_attribs['name'].append(file.relative_to(data_path))

df = pd.DataFrame.from_dict(file_attribs)

# Adding columns 
df['dial_visibility'] = -1
df['dial_visibility_p_0'] = -1
df['dial_visibility_p_1'] = -1
df['like'] = -1 
df['like_p_0'] = -1
df['like_p_1'] = -1
df['image_quality'] = -1

df.to_csv(csv_path, index=False)