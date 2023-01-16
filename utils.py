from bs4 import BeautifulSoup


def ecli_to_local_verdict_filename(ecli):
    return ecli.replace(":", "_") + ".xml"


def to_soup(content):
    return BeautifulSoup(content, "lxml")


def extract_verdicts(soup):
    return soup.find_all("entry")


def safe_find_text(soup, selector, attrs=None):
    finding = soup.find(selector, attrs=attrs)
    if finding:
        return finding.text
    else:
        return ""


def find_elements_containing(root: str, soup: BeautifulSoup, words: list):
    sections = soup.find_all(root)
    result = []
    for section in sections:
        for word in words:
            if word in section.text:
                result.append(section.text)
                continue
    return result


def find_griffier_text(soup):
    results = find_elements_containing(root="para", soup=soup, words=["griffier", "griffiers"])

    if results:
        return " ".join(results), True
    else:
        return None, False


def find_beslissing(soup):
    beslissings_text = ""
    beslissings_text += safe_find_text(soup, "section", {"role": "beslissing"})

    if beslissings_text:
        return beslissings_text, True

    full_text = safe_find_text(soup, "uitspraak")
    if full_text:
        return full_text, False
    else:
        return None, False
