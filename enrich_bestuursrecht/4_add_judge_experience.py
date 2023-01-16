from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from tqdm import tqdm

from models import Verdict, Person, ProfessionalDetail
from utils import cleanup, only_beslissings

new_judges = set()

def judge_experience(row):
    person = session.query(Person).filter(Person.toon_naam_kort.ilike(row['voorzitter_naam'])).first()
    if not person:
        print(row['ecli'], row['voorzitter_naam'])
        return row


    pd = session.query(ProfessionalDetail).filter_by(person_id=person.id).order_by(ProfessionalDetail.start_date.asc()).first()
    if not pd:
        print(row['ecli'], row['voorzitter_naam'])
        return row
    row['voorzitter_id'] = person.id
    row['voorzitter_start_date'] = pd.start_date
    row['experience_voorzitter_days'] = (row['issued'] - row['voorzitter_start_date']).days

    return row


engine = create_engine('postgresql://ors2user:ors2@localhost:54322/ors2')
Session = sessionmaker(bind=engine)
session = Session()

df = pd.read_excel('3_dataset_checked_people.xlsx')

tqdm.pandas()

df = df.progress_apply(judge_experience, axis=1)
df = df.sort_values(by=['ecli'])
df.to_excel('4_dataset_judge_experience.xlsx', index=False)
