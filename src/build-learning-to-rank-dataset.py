# -*- coding: utf-8 -*-

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter
from num2words import num2words
from nltk.probability import FreqDist
from string import punctuation

import nltk
import os
import string
import numpy as np
import copy
import pandas as pd
import pickle
import re
import math
import time
import json
import gc

def remove_stop_words(data):
    stemmer= PorterStemmer()
    stop_words = stopwords.words('portuguese')
    words = word_tokenize(str(data))
    new_text = ""
    for w in words:
        if w not in stop_words and len(w) > 1:
            new_text = new_text + " " + stemmer.stem(w)
    return new_text

def preprocess(data):
    return remove_stop_words(data)

def doc_freq(word):
    c = 0
    try:
        c = DF[word]
    except:
        pass
    return c

def streamSize(stream):
    if stream == None :
        return 0
    return len(stream.replace(" ", ""))

def clear_text(text):
    return re.sub("\s+", " ", re.sub("\n", "", re.sub("<[^>]+>", "", re.sub("[0-9]", "", text))))


dataset_base_path   = '$PATH'
datasets            = []
DF                  = {}
N                   = 0

inicio_total = time.time()
inicio = time.time()

for f in files:

    text = ""

    dataset_path = os.path.join(dataset_base_path, f, 'metadata.txt')

    if os.path.isfile(dataset_path):
        file = open(dataset_path)
        text = file.read().strip()
        file.close()
    if len(text) == 0:
        dataset_path = os.path.join(dataset_base_path, f, 'dataset.json')
        file = open(dataset_path, 'r')
        json_text = json.loads(file.read().strip())
        text = json_text.get("title") + " " + json_text.get("notes")
        file.close()

    datasets.append(preprocess(text))

N = len(datasets)

fim = time.time()

gc.collect()
inicio = time.time()

tokens = []

for i in range(N):
    token_id = 0
    tokens = datasets[i]
    for w in tokens:
        try:
            DF[w].add(i)
        except:
            DF[w] = {i}

        token_id +=1

for i in DF:
    DF[i] = len(DF[i])

doc = 0

tf_idf = {}
fim = time.time()

features = {}

gc.collect()
inicio = time.time()
tokens = []

for i in range(N):

    tfs     = []
    idfs    = []
    tf_idfs = []

    tokens = word_tokenize(datasets[i])

    counter = Counter(tokens)
    words_count = len(tokens)

    if words_count == 0:
        words_count = 1

    for token in np.unique(tokens):

        tf = counter[token]/words_count
        df = doc_freq(token)
        idf = np.log((N+1)/(df+1))

        tf_idf[doc, token] = tf*idf

        tfs.append(tf)
        idfs.append(idf)
        tf_idfs.append(tf*idf)

    media_tfs       = sum(tfs) / len(tfs)
    media_idfs      = sum(idfs) / len(idfs)
    media_tf_idfs   = sum(tf_idfs) / len(tf_idfs)
    title_size      = 0
    sumary_size     = 0
    tags_size       = 0
    group_size      = 0
    org_title_size  = 0
    author_size     = 0
    mantenedor_size = 0

    json_dir = os.path.join(dataset_base_path, files[doc], 'dataset.json')

    if os.path.isfile(json_dir):

        json_file = open(json_dir, 'r')
        dataset_json_file = json.loads(json_file.read())

        tags_list = []
        for tag in dataset_json_file.get("tags"):
            tags_list.append(tag.get("display_name"))

        organization = dataset_json_file.get("organization")
        tags_size    = len(tags_list)

        if (dataset_json_file.get("title") != None) :
            title_size = streamSize(dataset_json_file.get("title"))
        if (dataset_json_file.get("notes") != None) :
            sumary_size = streamSize(clear_text(dataset_json_file.get("notes")))
        if (dataset_json_file.get("groups") != None) :
            group_size = len(dataset_json_file.get("groups"))
        if (organization != None and organization.get("title") != None) :
            org_title_size  = streamSize(organization.get("title"))
        if (dataset_json_file.get("author") != None) :
            author_size = streamSize(dataset_json_file.get("author"))
        if (dataset_json_file.get("maintainer") != None) :
            mantenedor_size = streamSize(dataset_json_file.get("maintainer"))

    features[files[doc]] = (title_size, sumary_size, tags_size, group_size, org_title_size,
        author_size, mantenedor_size, min(tfs), max(tfs), sum(tfs), media_tfs, min(idfs),
        max(idfs), sum(idfs), media_idfs, min(tf_idfs), max(tf_idfs), sum(tf_idfs), 
        media_tf_idfs)

    tfs     = []
    idfs    = []
    tf_idfs = []
    doc += 1
    gc.collect()

fim = time.time()
gc.collect()

f = open("#PATH/all-features.txt", "w")
f.write(str(features))
f.close()
