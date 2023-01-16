from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from tqdm import tqdm

from models import Verdict
from outcome_utils import determine_outcome

def outcome_handler(row):
    verdict = session.query(Verdict).filter_by(id=row['id']).first()
    if row['hand_checked']:
        return row
    row['outcome'] = determine_outcome(verdict)
    return row

engine = create_engine('postgresql://ors2user:ors2@localhost:54322/ors2')
Session = sessionmaker(bind=engine)
session = Session()

df = pd.read_excel('2_dataset_with_outcome.xlsx')

tqdm.pandas()

df = df.progress_apply(outcome_handler, axis=1)
df = df.sort_values(by=['outcome'], ascending=False)
df.to_excel('2_dataset_with_outcome.xlsx', index=False)

print(len(df[df['hand_checked'] == 1]))

df = df.groupby('outcome').count()
print(df)