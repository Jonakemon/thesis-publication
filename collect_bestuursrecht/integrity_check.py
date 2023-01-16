def has_griffier(labels):
    return any('GRIFFIER' in sublist for sublist in labels)


def has_voorzitter(labels):
    return any('VOORZITTER' in sublist for sublist in labels)


def has_rechter(labels):
    return any('RECHTER' in sublist for sublist in labels)


from jsonlines import jsonlines

result = []

with jsonlines.open('judges.jsonl') as reader:
    for obj in reader:
        result.append(obj)

no_griffier = 0
no_rechter = 0
no_voorzitter = 0
bad_length = 0
no_labels = 0

for case in result:
    if not has_voorzitter(case.get("label")):
        print(case.get("meta"))
        no_voorzitter += 1
    if not has_rechter(case.get("label")):
        no_rechter += 1
    if not has_griffier(case.get("label")):
        no_griffier += 1
    if len(case.get("label")) not in (1, 3, 5):
        bad_length += 1
    if len(case.get("label")) == 0:
        no_labels += 1
print(no_voorzitter, no_rechter, no_griffier, bad_length, no_labels)
