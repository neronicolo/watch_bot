import shutil
from pathlib import Path

import pandas as pd

def filter_by_prediction(df, thresh_min, thresh_max, label):
    '''Filter images based on prediction thresh_min, thresh_max, value mad label. Return dataframe'''
    try:
        if (label == 0):
            df_filtered = df[df[['dial_visibility_p_0', 'dial_visibility_p_1']].max(1) > thresh_min]
            df_filtered = df_filtered[df_filtered[['dial_visibility_p_0', 'dial_visibility_p_1']].max(1) < thresh_max] 
        elif (label == 1):
            pass
        return df_filtered
    except (ValueError):
        print("Invalid Filter Pattern")
        return

def filter_by_image_size(df, size):
    '''Fiter images based on size. Return file list'''
    df = df[(df['image_size_x'] > size) & (df['image_size_y'] > size)]
    return df['name'].to_list()

data_path = Path.home()/'programming/data/chrono24'
dataset_path = Path.home()/'programming/data/watch_bot/chrono24_dial_visibility_most_uncertain/'
read_csv_path = Path.home()/'programming/data/chrono24/file_attribs_chrono24_add_inference.csv'
save_csv_path = Path.home()/'programming/projects/watch_bot/data_prep/chrono24_dial_visibility_most_uncertain.csv'

df = pd.read_csv(read_csv_path)
df = filter_by_prediction(df, 0.5, 0.6, 0)
#df.to_csv(save_csv_path, index=False)
files = filter_by_image_size(df, 300)
dataset_path.mkdir(exist_ok=True)

for file in files[:10]:
    shutil.copy(data_path/file, dataset_path)