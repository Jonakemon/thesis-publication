from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from tqdm import tqdm

from models import Verdict

engine = create_engine('postgresql://ors2user:ors2@localhost:54322/ors2')
Session = sessionmaker(bind=engine)
session = Session()

df = pd.read_excel('0_dataset_bestuursrecht.xlsx')
cases = df.to_dict('records')

for case in tqdm(cases):
    verdict = session.query(Verdict).filter_by(ecli=case.get("ecli")).first()
    case['issued'] = verdict.issued
    case['id'] = verdict.id
    case['institution'] = verdict.institution_id
    case['procedure_type'] = verdict.procedure_type_id

df = pd.DataFrame(cases)
df.to_excel('1_dataset_with_id_issued_institution.xlsx')