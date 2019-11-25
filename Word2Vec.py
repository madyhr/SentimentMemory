# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 16:49:57 2019

@author: Marcus Dyhr
"""

#import gensim

#model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary = True)

if "murder" in model:
    print("Its true!")
    print(model["murder"])
    print(model.most_similar("murder",topn=25))