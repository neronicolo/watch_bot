from fastai.vision import *
from tqdm import tqdm

# TODO: make cli version of this program:
#   file_attrib(source folder(starting folder for recursion), csv_path(where to save), **kwargs(column for labelin))

data_path =  Path.home()/'programming/data/chrono24'
csv_path = data_path/'file_attribs_inference.csv'

files = sorted(data_path.rglob('.jpg'))
file_attribs = defaultdict(list)

for file in files:
    