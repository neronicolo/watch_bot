import check
import regex
import pandas as pd
from pathlib import Path
import collections
from tqdm import tqdm

path = check.path_check(Path.home()/"programming/data/watch_bot/")
file_iterator = check.gen_check(path.rglob('*.jpg'))
file_attribs = collections.defaultdict(list)

# TODO: How to get better looking progers bar with tqdm, look at fastclass or tqdm docs
# TODO: Check which attributes(colums) we need to create 
# TODO: Test if is an image, is needed? import imghdr vs PIL. fastClass cwegner git
# TODO: Move logic to def main()? if __name__ == "__main__":
# TODO: Do I need sorted?
for file in tqdm(file_iterator):
    file_attribs['name'].append(file.relative_to(path))
    #file_attribs['image_size'].append()

df = pd.DataFrame.from_dict(file_attribs)
df.to_csv(path/'watch_face_classifier_file_attribs.csv', index=False)