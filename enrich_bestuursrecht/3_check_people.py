from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from tqdm import tqdm

from models import Verdict
from utils import cleanup, only_beslissings

with open('griffiers.txt', 'r') as f:
    griffiers = [line.strip() for line in f]

with open('judges.txt', 'r') as f:
    judges = [line.strip() for line in f]

def find_griffier(text):
    for griffier in griffiers:
        hit = text.find(griffier)
        if hit > 0:
            return griffier


def find_voorzitter(text):
    labels = []

    for judge in judges:
        hit = text.find(judge)
        if hit > 1:
            temp = [hit, hit + len(judge), 'RECHTER', judge]
            labels.append(temp)

    if not labels:
        return None
    elif len(labels) == 1:
        return labels[0][3]
    else:
        labels.sort(key=lambda x: (x[0], -x[1]))
        return labels[0][3]


def people_check_handler(row):
    verdict = session.query(Verdict).filter_by(id=row['id']).first()
    text = only_beslissings(cleanup(verdict.beslissings_text))
    row['new_griffier'] = find_griffier(text)
    if row['griffier_naam'] != row['new_griffier']:
        print(f'griffier {verdict.ecli} mismatch: {row["griffier_naam"]} -> {row["new_griffier"]}')
    return row


engine = create_engine('postgresql://ors2user:ors2@localhost:54322/ors2')
Session = sessionmaker(bind=engine)
session = Session()

df = pd.read_excel('4_dataset_judge_experience.xlsx')

tqdm.pandas()

df = df.progress_apply(people_check_handler, axis=1)
df = df.sort_values(by=['outcome'], ascending=False)
df.to_excel('4_dataset_judge_experience.xlsx', index=False)
