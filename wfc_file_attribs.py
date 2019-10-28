import check
import pandas as pd
from pathlib import Path
from PIL import Image
import collections
from tqdm import tqdm


dir_path = check.path_check(Path.home()/"programming/data/watch_bot/")
file_iterator = check.gen_check(dir_path.rglob('*.jpg'))
file_attribs = collections.defaultdict(list)

# TODO: Check which attributes(colums) we need to create 

for file in tqdm(file_iterator):
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

# Remove rows where image_size_x and image_size_y are less than size.
size = 300
df = df[(df['image_size_x'] > size) & (df['image_size_y'] > size)]

#Add columns for labeling
df['watch_face_visibility'] = -1
df['composition_quality'] = -1
df['light_quality'] = -1
df['image_quality'] = -1

print(shape_init, df.shape)
df.to_csv(dir_path/'wfc_file_attribs.csv', index=False)
