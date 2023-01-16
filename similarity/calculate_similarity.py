import logging
import pandas as pd
from gensim.models.doc2vec import Doc2Vec
from gensim import utils
from tqdm import tqdm

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model = Doc2Vec.load('docmodel')

df_verdicts = pd.read_pickle('ecli_and_texts.pickle')
verdicts = df_verdicts.to_dict('records')

dataset = pd.read_excel('dataset.xlsx')

for verdict in tqdm(verdicts):
    # retrieve the text for each verdict, preprocesses the text and compares the text to the corpus
    text = verdict.pop('text')
    tokens = utils.simple_preprocess(text)
    vector = model.infer_vector(tokens)

    # we retrieve the 25 most similar verdicts, retrieve the metadata of each verdict from our dataset and exclude verdicts that were written by the same assistant
    similar_verdicts = model.dv.most_similar([vector], topn=25)
    metadata_verdict = dataset.loc[dataset['ecli'] == verdict.get('ecli')].to_dict('records')[0]
    for doc in similar_verdicts:
        doc_metadata = dataset.loc[dataset['ecli'] == doc[0]].to_dict('records')[0]
        if metadata_verdict['griffier_naam'] == doc_metadata['griffier_naam']:
            continue
        else:
            verdict['most_similar_ecli'] = doc[0]
            verdict['similarity_score'] = doc[1]
            break

# save dataset with similarity
df = pd.DataFrame(verdicts)
df.to_excel('dataset_with_similarity.xlsx')
