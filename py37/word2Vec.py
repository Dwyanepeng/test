#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/1 11:49
# @Site    : 
# @File    : word2Vec.py
# @Software: PyCharm

import gensim, logging, os
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import nltk
nltk.download('brown')
corpus = nltk.corpus.brown.sents()

fname = 'brown_skipgram.model'
if os.path.exists(fname):
    model = gensim.models.Word2Vec.load(fname)
else:
    model = gensim.models.Word2Vec(corpus, size=100, min_count=5, workers=2, iter=50)
    model.save(fname)