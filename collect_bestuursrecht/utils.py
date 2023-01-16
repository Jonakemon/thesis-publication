import re

def only_beslissings(text):
    if len(text) > 1500:
        i = text.find('Beslissing')
        if i > 0:
            return text[i:]
    return text


def cleanup(text):
    text = text.replace("\n", " ")
    text = text.replace(" ", " ")
    text = re.sub(' +', ' ', text)
    return bytes(text, 'utf-8').decode('utf-8', 'ignore')
