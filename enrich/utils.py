import re

from bs4 import BeautifulSoup


def ecli_to_local_verdict_filename(ecli):
    return ecli.replace(":", "_") + ".xml"

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


def safe_find_int(soup, selector, attrs=None, default=0):
    finding = soup.find(selector, attrs=attrs)
    if finding:
        return int(finding.text)
    else:
        return default

