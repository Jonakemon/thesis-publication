import logging
import pandas as pd
from gensim import utils
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

df = pd.read_pickle('ecli_and_texts.pickle')
corpus = df.to_dict('records')


class Corpus:
    def __iter__(self):
        for verdict in corpus:
            tokens = utils.simple_preprocess(verdict.get('text'))
            yield TaggedDocument(tokens, [verdict.get('ecli')])


verdicts = Corpus()
model = Doc2Vec(vector_size=100, min_count=2)
model.build_vocab(verdicts)
model.train(verdicts, total_examples=model.corpus_count, epochs=model.epochs)

model.save('docmodel')
