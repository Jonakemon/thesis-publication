from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from tqdm import tqdm

from models import Verdict, Person, ProfessionalDetail
from utils import cleanup, only_beslissings

new_judges = set()

def griffier_experience(row):
    row['experience_griffier_days'] = (row['issued'] - row['griffier_start_date']).days
    return row


df = pd.read_excel('4_dataset_judge_experience.xlsx')

tqdm.pandas()

df = df.progress_apply(griffier_experience, axis=1)
df = df.sort_values(by=['ecli'])
df.to_excel('6_dataset_griffier_experience.xlsx', index=False)
