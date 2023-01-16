import re

from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

from utils import ecli_to_local_verdict_filename

ECLI_PATTERN = 'ECLI:[A-Z]{2}:.{1,7}:\d{4}:[a-zA-Z\d\.]{1,25}'


def count_ecli_references(soup):
    uitspraak = soup.find('uitspraak').find_all(text=True)
    text = " ".join(uitspraak).replace("\n", "")
    matches = re.findall(ECLI_PATTERN, text)
    return len(matches)


def verdict_length(soup):
    uitspraak = soup.find('uitspraak').find_all(text=True)
    text = " ".join(uitspraak).replace("\n", "")
    return len(text)


def calculate_complexity(row):
    filename = ecli_to_local_verdict_filename(row['ecli'])
    path = '../2020_bestuursrecht/' + filename
    soup = BeautifulSoup(open(path), "lxml")
    row['complexity_ecli_references'] = count_ecli_references(soup)
    row['complexity_verdict_length'] = verdict_length(soup)
    return row


df = pd.read_excel('7_dataset_relative_experience.xlsx')

tqdm.pandas()

df = df.progress_apply(calculate_complexity, axis=1)
df.to_excel('8_dataset_with_verdict_length_and_ecli.xlsx', index=False)
