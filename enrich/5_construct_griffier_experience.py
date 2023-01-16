import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from tqdm import tqdm

from models import Verdict, Person, ProfessionalDetail
from utils import cleanup, only_beslissings

SEARCH_ENDPOINT = "https://uitspraken.rechtspraak.nl/api/zoek"
DEFAULT_LIMIT = 1000
DEFAULT_SEARCH_QUERY_PARAMS = {"StartRow": 0, "PageSize": 10, "ShouldReturnHighlights": True,
                               "ShouldCountFacets": True, "SortOrder": "UitspraakDatumAsc", "Contentsoorten": [],
                               "Rechtsgebieden": [],
                               "DatumPublicatie": [], "DatumUitspraak": [],
                               "Advanced": {"PublicatieStatus": "AlleenGepubliceerd"},
                               "CorrelationId": "4c9c088a773549c28fe561e8e9b73ca7", "Proceduresoorten": []}


def find_first_occurence(griffier, instantie):
    griffier = griffier.replace("-", " ").replace("'", " ")
    search_term = [{"Term": f"\"{griffier}\"", "Field": "AlleVelden"}]
    instanties = [{"NodeType": 2,
                   "Identifier": instantie,
                   "level": 2}]

    r = requests.post(SEARCH_ENDPOINT, json={**DEFAULT_SEARCH_QUERY_PARAMS, "SearchTerms": search_term})

    if not r.ok or r.url == "https://mededeling.rechtspraak.nl/404":
        print(f"Error during verdict collection: STATUS_CODE {r.status_code} | URL {r.url} | CONTENT {r.content}")

    response = r.json()
    results = response.get("Results")

    if not results:
        print(f"Error, no cases found for {griffier}")
        return {"naam": griffier,
            "date_first_case": None,
            "ecli_first_case": '',
            "total_cases_found": 0}

    first_result = results[0]
    return {"naam": griffier,
            "date_first_case": first_result.get("Uitspraakdatum"),
            "ecli_first_case": first_result.get("TitelEmphasis"),
            "total_cases_found": response.get("ResultCount")}


from griffiers_to_find_experience import GRIFFIERS

result = []
for tup in tqdm(GRIFFIERS):
    fo = find_first_occurence(tup[0], tup[1])
    result.append(fo)

df = pd.DataFrame(result)
df.to_excel('5_griffier_experience.xlsx')