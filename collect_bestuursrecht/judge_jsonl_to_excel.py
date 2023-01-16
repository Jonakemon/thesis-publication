import pandas as pd
from jsonlines import jsonlines

result = []

def to_ecli(link):
    return link[52:]

with jsonlines.open('judges.jsonl') as reader:
    for case in reader:
        labels = case.get('label')
        vz = None
        for label in labels:
            if label[2] == 'VOORZITTER':
                vz = case.get('text')[label[0]:label[1]]
        result.append({'ecli': to_ecli(case.get('meta')), 'voorzitter': vz, 'judge_count': len(labels)})


df = pd.DataFrame(result)
df.to_excel('judges_ecli.xlsx')