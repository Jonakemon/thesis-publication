import requests
import pandas as pd
from tqdm import tqdm

from utils import ecli_to_local_verdict_filename

BASE_URL = 'https://linkeddata.overheid.nl/service/get-aantal-per-informatietype?ext-id='


def get_aantal(ecli):
    r = requests.get(BASE_URL + ecli)
    r.raise_for_status()

    with open('lido_result/lido_' + ecli_to_local_verdict_filename(ecli), 'wb') as f:
        f.write(r.content)


def calculate_complexity(row):
    get_aantal(row['ecli'])


df = pd.read_excel('8_dataset_with_verdict_length_and_ecli.xlsx')
tqdm.pandas()
df = df.progress_apply(calculate_complexity, axis=1)
