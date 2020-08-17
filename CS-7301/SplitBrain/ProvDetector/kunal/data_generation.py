from __future__ import division, print_function

import numpy as np
from sklearn.model_selection import train_test_split
from gensim.models.doc2vec import Doc2Vec

import argparse

import copy
from random import shuffle
from os import path
import pandas as pd
import csv

from train_doc2vec import *
from data_loader import *

trials = 5
model_location="models"
USE_CACHE=False

model_map = dict()
docs_map = dict()
config_map = dict()

def get_model(app, benign, anomaly):
    model_name = model_location+"/"+app+".model"
 
    if model_name in model_map:
        return model_map[model_name]  
    elif path.exists(model_name):
        model = Doc2Vec.load(model_name)
        model_map[model_name] = model
        return model
 
    data = benign + anomaly
    vector_size = 50
    epochs = 100
    if app in config_map:
        epochs = config_map[app].dict['epochs'] 
    model = train_doc2vec(data, vector_size, epochs)
    if USE_CACHE:
        model_map[model_name] = model
    # model.save(model_name)
    print("Model Built: %s" % model_name)
    return model

def run(app, cur_iter=0):
    benign_loader = PathDataLoader(app, True) 
    anomaly_loader = PathDataLoader(app, False) 
    if app in config_map:
        benign_loader.config = config_map[app]   
        anomaly_loader.config = config_map[app]   
 
    if app not in docs_map:
        benign_paths = benign_loader.load_paths() # 2 was added
        anomaly_paths = anomaly_loader.load_paths() # 2 was added
        benign_docs = [path.to_words() for path in benign_paths]
        anomaly_docs = [path.to_words() for path in anomaly_paths]
        docs_map[app] = (benign_docs, anomaly_docs)
    else:
        benign_docs, anomaly_docs = docs_map[app]

    if cur_iter == 0: 
        print("Samples benign and anomaly: %d\t%d" % (len(benign_docs), len(anomaly_docs)))   

    if len(benign_docs)==0 or len(anomaly_docs)==0:
        return (0, 0)
    
    benign_doc_train, benign_doc_test = train_test_split(benign_docs, test_size=0.25)
    shuffle(anomaly_docs)
    anomaly_size = len(benign_doc_test)
    anomaly_docs_test = anomaly_docs[0:anomaly_size]  
 
    model = get_model(app, benign_docs, anomaly_docs_test)
    infer_epochs = model.epochs

    benign_data = []
    for item in benign_doc_train:
        x = model.infer_vector(item, epochs=infer_epochs)
        benign_data.append(x)

    benign_data_test = []
    for item in benign_doc_test:
        x = model.infer_vector(item, epochs=infer_epochs)
        benign_data_test.append(x)
    
    anomaly_data = []
    for item in anomaly_docs_test:
        x = model.infer_vector(item, epochs=infer_epochs)
        anomaly_data.append(x)

    # save the data
    pd.DataFrame(benign_data).to_csv('kunal_data/benignK.csv')
    pd.DataFrame(benign_data_test).to_csv('kunal_data/benignTestK.csv')
    pd.DataFrame(anomaly_data).to_csv('kunal_data/anaK.csv')


def run_multiple(app):
    run(app, 0)


results = []
apps=["winword"]
run_multiple(apps[0])



