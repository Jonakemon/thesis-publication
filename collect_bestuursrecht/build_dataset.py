import json
import re

from jsonlines import jsonlines
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from tqdm import tqdm

from utils import only_beslissings, cleanup
from models import Verdict, PersonVerdict, Person
from eclis import eclis



engine = create_engine('postgresql://ors2user:ors2@localhost:54322/ors2')
Session = sessionmaker(bind=engine)
session = Session()

result = []

for ecli in tqdm(eclis):
    verdict = session.query(Verdict).filter_by(ecli=ecli).first()

    if "wraking" in verdict.beslissings_text:
        continue

    people = session.query(Person).join(PersonVerdict).filter(PersonVerdict.verdict_id == verdict.id).all()
    text = cleanup(only_beslissings(verdict.beslissings_text))

    t = {'text': text, 'meta': {'ecli': verdict.ecli}}
    labels = []
    for p in people:
        TYPE = "RECHTER"
        if len(people) == 1:
            TYPE = "VOORZITTER"

        hit = text.find(p.toon_naam_kort)
        temp = [hit, hit + len(p.toon_naam_kort), TYPE]
        labels.append(temp)

    index = None
    first = 99999999
    for i, label in enumerate(labels):
        if label[0] < first:
            first = label[0]
            index = i

    if index:
        labels[index][2] = 'VOORZITTER'

    t['label'] = labels

    pattern = re.compile('((?!.*heid) .+?)(, griffier)')
    hits = pattern.search(text)
    if hits:
        griffier = hits[1].replace("van", "", 1).strip()
        hit = text.find(griffier)
        temp = [hit, hit + len(griffier), "GRIFFIER"]
        t['label'].append(temp)
    result.append(t)

with jsonlines.open('new.jsonl', mode='w') as writer:
    writer.write_all(result)
