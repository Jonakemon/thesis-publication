from jsonlines import jsonlines
import pandas as pd

result = []

JUDGE_DEFINITION = ['VOORZITTER', 'RECHTER']
GRIFFIER_DEFINITION = ['GRIFFIER']
judges = set()
griffiers = set()

with jsonlines.open('tagged.jsonl') as reader:
    for case in reader:
        for label in case.get("label"):
            name = case.get("data")[label[0]:label[1]]
            type = label[2]
            if type in JUDGE_DEFINITION:
                judges.add(name)
            else:
                griffiers.add(name)

f = open("judges.txt", "a")
f.write('\n'.join(judges))
f.close()

f = open("griffiers.txt", "a")
f.write('\n'.join(griffiers))
f.close()
