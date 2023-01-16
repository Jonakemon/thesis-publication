import shutil

from collect_bestuursrecht.eclis import eclis
from utils import ecli_to_local_verdict_filename

for ecli in eclis:
    filename = ecli_to_local_verdict_filename(ecli)
    src_path = '../rechtspraak-analyse/2020/' + filename
    dest_path = '2020_bestuursrecht/' + filename
    print(f"{src_path} => {dest_path}")
    shutil.copy(src_path, dest_path)
