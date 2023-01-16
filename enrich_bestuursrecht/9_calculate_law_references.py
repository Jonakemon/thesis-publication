import re

from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

from utils import ecli_to_local_verdict_filename, safe_find_int


def calculate_law_references(ecli):
    with open('lido_result/lido_' + ecli_to_local_verdict_filename(ecli), 'r') as f:
        xml = f.read()
        soup = BeautifulSoup(xml, 'lxml')

    wetten = safe_find_int(soup, 'aantal', {'informatietype': 'http://linkeddata.overheid.nl/terms/Wet'})
    mstr_regeling = safe_find_int(soup, 'aantal', {'informatietype': 'http://linkeddata.overheid.nl/terms/MinisterieleRegeling'})
    verdrag = safe_find_int(soup, 'aantal', {'informatietype': 'http://linkeddata.overheid.nl/terms/Verdrag'})
    return wetten + mstr_regeling + verdrag


def calculate_complexity(row):
    row['complexity_law_references'] = calculate_law_references(row['ecli'])
    return row


df = pd.read_excel('8_dataset_with_verdict_length_and_ecli.xlsx')
tqdm.pandas()
df = df.progress_apply(calculate_complexity, axis=1)
df.to_excel('9_dataset_with_law_references.xlsx', index=False)
