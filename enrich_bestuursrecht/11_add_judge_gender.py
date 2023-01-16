import re

from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

from models import Person
from utils import ecli_to_local_verdict_filename, safe_find_int


def add_gender(row):
    vz = session.query(Person).filter_by(id=row['voorzitter_id']).first()
    row['gender'] = vz.gender
    return row


engine = create_engine('postgresql://ors2user:ors2@localhost:54322/ors2')
Session = sessionmaker(bind=engine)
session = Session()

df = pd.read_excel('10_dataset_with_complexity_index.xlsx')
tqdm.pandas()
df = df.progress_apply(add_gender, axis=1)
df.to_excel('11_dataset_with_gender.xlsx', index=False)
