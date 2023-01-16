import pandas as pd
from tqdm import tqdm


def relative_experience(row):
    vz = row['experience_voorzitter_days']
    grif = row['experience_griffier_days']
    row['relative_experience'] = vz - grif
    return row

df = pd.read_excel('6_dataset_griffier_experience.xlsx')

tqdm.pandas()

df = df.progress_apply(relative_experience, axis=1)
df.to_excel('7_dataset_relative_experience.xlsx', index=False)
