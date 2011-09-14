'''

input is a LSI model (created with LSI model run)
input is a preprocessing model
input is a dictionary

reimplement the fridolin paper

evaluate one of our trained models with the data from the fridolin paper

Parameters driving effectiveness of automated essay scoring with LSA
citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.87.4534&rep=rep1&type=pdf

@author: dedan
'''

from gensim import utils
from gensim.corpora.dictionary import Dictionary
from gensim.corpora.textfilescorpus import TextFilesCorpus
from gensim.gensim.models.logentropy_model import LogEntropyModel
from gensim.gensim.utils import SaveLoad
from gensim.models.lsimodel import LsiModel
from gensim.similarities.docsim import MatrixSimilarity
from scipy import stats
from os import path
import Stemmer
import glob
import numpy as np
import re
import string
import sys
import tools

def main(param_file=None):

    # setup
    p, base_path, output_dir = tools.setup(param_file)
    model_path = path.join(base_path,
                           p['result_path'],
                           p['model_label'])
    logger = tools.get_logger('gensim', path.join(output_dir, "run.log"))
    logger.info("running %s" % ' '.join(sys.argv))

    # train the model on the small marketing corpus
    preprocess = []

    if 'stoplist' in p.as_dict():
        stoplist = open(path.join(base_path, p['stoplist'])).readlines()
        stoplist = [unicode(s.strip(), encoding='utf-8').lower() for s in stoplist]
        def remove_stopwords(sentence):
            return [word for word in sentence if not word in stoplist]
        preprocess.append(remove_stopwords)

    if 'stemmer' in p.as_dict():
        stemmer = Stemmer.Stemmer(p['stemmer'])
        preprocess.append(stemmer.stemWords)

    if not p['model_label']:
        cor = TextFilesCorpus(path.join(base_path, p['corpus_path']),
                              no_below=p['no_below'],
                              no_above=p['no_above'],
                              preprocess=preprocess)
        dictionary = cor.dictionary

        pre = LogEntropyModel(cor, id2word=dictionary, normalize=True)
        lsi = LsiModel(pre[cor], id2word=dictionary, num_topics=p['num_topics'])
    else:
        dictionary = Dictionary.load(path.join(model_path, p['dict_name']))
        pre = SaveLoad.load(path.join(model_path, 'pre.model'))
        lsi = LsiModel.load(path.join(model_path, 'lsi.model'))
        lsi.num_topics = p['num_topics']

    test_cor_path = path.join(base_path, p['test_cor_path'])
    test_answers, gold_answers, ratings = [], [], []


    flist = glob.glob(path.join(test_cor_path, 'corpus_3', '*.txt'))
    for file in flist:
        match = re.search('data3_(\d)_\d+.txt', file)
        ratings.append(int(match.group(1)))
        with open(file) as f:
            doc = string.join(map(string.strip, f.readlines()))
            doc = utils.tokenize(doc, lower=True)
            for func in preprocess:
                doc = func(doc)
            corpus = lsi[pre[dictionary.doc2bow(doc)]]
            test_answers.append(corpus)
    flist = glob.glob(path.join(test_cor_path, 'corpus_3_golden', '*.txt'))
    for file in flist:
        with open(file) as f:
            doc = string.join(map(string.strip, f.readlines()))
            doc = utils.tokenize(doc, lower=True)
            for func in preprocess:
                doc = func(doc)
            corpus = lsi[pre[dictionary.doc2bow(doc)]]
            gold_answers.append(corpus)


    sim = MatrixSimilarity(test_answers)[gold_answers]
    mean_sim = np.mean(sim, axis=0)
    print 'pearsons corrcoef: %f' % np.corrcoef(ratings, mean_sim)[0,1]
    print 'spearmans r: %f with p: %f' % stats.spearmanr(ratings, mean_sim)

if __name__ == '__main__':
    main()