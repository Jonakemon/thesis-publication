import string

from jsonlines import jsonlines
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

from utils import only_beslissings, cleanup
from models import Verdict, PersonVerdict, Person
from eclis import eclis

engine = create_engine('postgresql://ors2user:ors2@localhost:54322/ors2')
Session = sessionmaker(bind=engine)
session = Session()

result = []

with open('judges.txt', 'r') as f:
    judges = [line.strip() for line in f]

no_labels = []

for ecli in tqdm(eclis):
    verdict = session.query(Verdict).filter_by(ecli=ecli).first()

    if "wraking" in verdict.beslissings_text:
        continue

    people = session.query(Person).join(PersonVerdict).filter(PersonVerdict.verdict_id == verdict.id).all()
    text = cleanup(only_beslissings(verdict.beslissings_text))

    t = {'text': text, 'meta': 'https://uitspraken.rechtspraak.nl/inziendocument?id=' + verdict.ecli}
    labels = []

    for judge in judges:
        hit = text.find(judge)
        if hit > 1:
            temp = [hit, hit + len(judge), 'RECHTER']
            labels.append(temp)

    if not labels:
        no_labels.append(ecli)
        result.append(t)
    elif len(labels) == 1:
        labels[0][2] = 'VOORZITTER'
    else:
        index = None
        first = 99999999
        labels.sort(key=lambda x: (x[0], -x[1]))
        labels[0][2] = 'VOORZITTER'

    labels = [list(x) for x in set(tuple(x) for x in labels)]
    t['label'] = labels
    result.append(t)

print(no_labels)

with jsonlines.open('judges.jsonl', mode='w') as writer:
    writer.write_all(result)
