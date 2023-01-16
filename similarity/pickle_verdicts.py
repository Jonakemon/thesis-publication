import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from eclis import ECLIS, TEST_ECLIS
from utils import ecli_to_local_verdict_filename


def verdict_text(soup):
    uitspraak = soup.find('uitspraak').find_all(text=True)
    text = " ".join(uitspraak).replace("\n", "")
    return text


r = []
for ecli in tqdm(ECLIS):
    path = f'../2020_bestuursrecht/{ecli_to_local_verdict_filename(ecli)}'
    soup = BeautifulSoup(open(path), "lxml")
    r.append({"ecli": ecli, "text": verdict_text(soup)})

df = pd.DataFrame(r)
df.to_pickle('dataset.pickle')
