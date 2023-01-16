import re

from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

from utils import ecli_to_local_verdict_filename, safe_find_int


def calculate_complexity_index(row):
    row['complexity_index'] = (row['complexity_verdict_length'] / 1000) + row['complexity_ecli_references'] + row['complexity_law_references']
    return row


df = pd.read_excel('9_dataset_with_law_references.xlsx')
tqdm.pandas()
df = df.progress_apply(calculate_complexity_index, axis=1)
df.to_excel('10_dataset_with_complexity_index.xlsx', index=False)
