import json
import re

from jsonlines import jsonlines
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm
import pandas as pd

from utils import only_beslissings, cleanup
from models import Verdict, PersonVerdict, Person
from eclis import eclis

engine = create_engine('postgresql://ors2user:ors2@localhost:54322/ors2')
Session = sessionmaker(bind=engine)
session = Session()

result = []

with open('griffiers.txt', 'r') as f:
    griffiers = [line.strip() for line in f]

for ecli in tqdm(eclis):
    verdict = session.query(Verdict).filter_by(ecli=ecli).first()

    if "wraking" in verdict.beslissings_text:
        continue

    # people = session.query(Person).join(PersonVerdict).filter(PersonVerdict.verdict_id == verdict.id).all()
    text = cleanup(verdict.beslissings_text)
    t = {'ecli': verdict.ecli}

    for griffier in griffiers:
        hit = text.find(griffier)
        if hit > 0:
            t['griffier'] = griffier
            break
    result.append(t)

df = pd.DataFrame(result)
df.to_excel('griffiers_ecli.xlsx')