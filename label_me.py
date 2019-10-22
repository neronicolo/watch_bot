import check
import collections
import pandas as pd
from PIL import Image
from pathlib import Path

dir_path = check.path_check(Path.home()/'programming/data/watch_bot/')
df = pd.read_csv(dir_path/'wfc_file_attribs.csv')

file_name = df['name'][0]
img = Image.open(dir_path/file_name)
img.show()