from fastai.vision import *
from tqdm import tqdm

# TODO: make cli version of this program:
#   file_attrib(source folder(starting folder for recursion), csv_path(where to save), **kwargs(column for labelin))

data_path =  Path.home()/'programming/data/chrono24/'
csv_path = data_path/'file_attribs_inference.csv'

files = sorted(data_path.rglob('*.jpg'))
file_attribs = defaultdict(list)

learn = load_learner(data_path)
learn = learn.to_fp32()

for file in tqdm(files[:10]):
    try:
        img = open_image(file)
        p_class, p_idx, p = learn.predict(img)
    except OSError:
        continue
    file_attribs['name'].append(file.relative_to(data_path))
    file_attribs['dial_visibility'].append(p_idx.tolist())
    file_attribs['dial_visibility_p_0'].append(p.tolist()[0])
    file_attribs['dial_visibility_p_1'].append(p.tolist()[1])
    file_attribs['like'].append(-1)
    file_attribs['like_p_0'].append(-1)
    file_attribs['like_p_1'].append(-1)

df = pd.DataFrame.from_dict(file_attribs)
df.to_csv(csv_path, index=False)
