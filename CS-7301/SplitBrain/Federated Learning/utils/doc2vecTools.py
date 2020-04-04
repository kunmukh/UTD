#!/usr/bin/env python3.6

# Kunal Mukherjee
# 4/3/20
# Federated Learning of Encoders and word2vec

import numpy as np
import pandas as pd
import gensim
from keras.models import Model, load_model
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
import datetime
import smart_open
from functools import reduce

from utils import dateFormat

# dict of model files
dictModelFName = dict({'encoder': "models/model_seqs2.h5",
                       'doc2vec': "models/doc2vecModel.pickle",
                       'doc2vecUpdated': "models/doc2vecModelUpdated.pickle"})


# function to create a taggedDocument or tokenzie a Document
def readCorpus(fname, tokens_only=False):
    with smart_open.open(fname, encoding="iso-8859-1") as f:
        for i, line in enumerate(f):
            tokens = gensim.utils.simple_preprocess(line)
            if tokens_only:
                yield tokens
            else:
                # For training data, add tags
                yield gensim.models.doc2vec.TaggedDocument(tokens, [i])


# generate the training and testing corpus
def dataProcessing(fileName, flag):
    corpus = None

    if flag is 'train':
        # generate the training and testing corpus
        corpus = list(readCorpus(fileName))
    elif flag is 'test':
        corpus = list(readCorpus(fileName, tokens_only=True))

    # print(pd.DataFrame(data=train_corpus))
    # print(pd.DataFrame(data=test_corpus))

    return corpus


# utility for testing doc2vec model
# infer the feature for the test_corpus from the doc2vec model
def DoctoVecFeatureInfer(doc2vecmodel, test_corpus):
    num_features = 100

    # extract the feature vector for each corpus in the test corpus
    feature_vec_test = np.empty((0, num_features))
    for i, corpus in enumerate(test_corpus):
        feature_vec_test = np.append(feature_vec_test, [doc2vecmodel.infer_vector(corpus)], axis=0)

    print(" Feature Test Vector: \n", pd.DataFrame(data=feature_vec_test).head())
    # print("Test Vec", np.asarray(feature_vec_test).shape)

    # normalize it
    # feature_vec_test = MinMaxScaler().fit_transform(feature_vec_test)
    # print(feature_vec_test)

    return feature_vec_test


# predict the in-lier and out-lier
def prediction(doc2vecmodel, test_corpus, feature_vec_train):
    # PREDICTION STEP
    autoencoder = load_model(dictModelFName['encoder'])

    # Testing the model
    feature_vec_test = DoctoVecFeatureInfer(doc2vecmodel, test_corpus)

    # combine test and train feature vec
    feature_vec = np.concatenate((feature_vec_train, feature_vec_test), axis=0)

    # predict it
    predicted = autoencoder.predict(feature_vec)

    return feature_vec, predicted


# use mean sq. error to calculate anomaly
def meanSqError (feature_vec, predicted_vec):
    # get the error term
    mse = np.mean(np.power(feature_vec - predicted_vec, 2), axis=1)

    # now add them to our data frame
    seqs_ds = pd.DataFrame(data={'line #': [i for i in range(0, feature_vec.shape[0])]})

    seqs_ds['MSE'] = mse

    print(seqs_ds)

    # getting the threshold
    # TODO: test threshold hyper parameters org:0.9997
    mse_threshold = np.quantile(seqs_ds['MSE'], 0.899)
    print('\n' + f'MSE 0.9997 threshold:{mse_threshold}' + '\n')

    # updating the MSE Outlier
    seqs_ds['MSE_Outlier'] = 0
    seqs_ds.loc[seqs_ds['MSE'] > mse_threshold, 'MSE_Outlier'] = 1

    print(seqs_ds)

    print('\n' + f"Num of MSE outlier:{seqs_ds['MSE_Outlier'].sum()}" + '\n')

    feature_vec_inlier_indices  = seqs_ds['MSE_Outlier'] <= 0
    feature_vec_outlier_indices = seqs_ds['MSE_Outlier'] > 0

    feature_vec_inlier = np.asarray(feature_vec)[feature_vec_inlier_indices]
    feature_vec_outlier = np.asarray(feature_vec)[feature_vec_outlier_indices]

    print("Inlier or Outlier:")
    print("% of Inlier :", len(feature_vec_inlier) / len(seqs_ds['MSE_Outlier']))
    print("% of Outlier:", len(feature_vec_outlier) / len(seqs_ds['MSE_Outlier']))

    return feature_vec_inlier, feature_vec_outlier


# plot the TSNE plot
def plotTSNE(feature_vec_train, feature_vec_inlier, feature_vec_outlier):
    # Plot using TSNE
    plt.title('T-SNE')

    tsne = TSNE(n_components=2, perplexity=50, n_iter=300)

    # plotting Training feature vector using TSNE
    tsne_results_train = tsne.fit_transform(feature_vec_train)
    plt.scatter(tsne_results_train[:, 0], tsne_results_train[:, 1], c='black')

    # in-lier feature vector
    tsne_results_vec = tsne.fit_transform(feature_vec_inlier)
    plt.scatter(tsne_results_vec[:, 0], tsne_results_vec[:, 1], c='blue')

    # out-lier feature vector
    if len(feature_vec_outlier) > 1:
        tsne_results_vec = tsne.fit_transform(feature_vec_outlier)
        plt.scatter(tsne_results_vec[:, 0], tsne_results_vec[:, 1], c='red')


# test doc2vec model
def testdoc2vecModel(modelName, testFileName):

    doc2vecModel = gensim.models.Doc2Vec.load(dictModelFName[modelName])
    # get the test corpus
    test_corpus = dataProcessing(testFileName, 'test')
    # get the feature vector
    feature_vec = doc2vecModel[doc2vecModel.wv.vocab]
    # get the prediction of the inlier and outlier from the test_corpus
    updated_feature_vec, pred = prediction(doc2vecModel, test_corpus, feature_vec)
    # get the meanSqError from the feature_vec_test, predicition_vec, feature_vec_train
    feature_vec_inlier, feature_vec_outlier = meanSqError(updated_feature_vec, pred)
    # plot the TSNE
    plotTSNE(feature_vec, feature_vec_inlier, feature_vec_outlier)

    # save the accuracy plot
    plt.savefig('img/TSNEPlot_' + dateFormat.getDate(str(datetime.datetime.now().date())) + '.png', dpi=100)
    plt.clf()


# generate the doc2vec model for the input doc
def createDoctoVecModel(train_corpus):
    # TODO: update the hyper parameters of model
    # generate the model for the training document
    model = gensim.models.doc2vec.Doc2Vec(min_count=2, epochs=40)
    # build the vocab
    model.build_vocab(train_corpus)
    # train the model
    model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
    # save the doc2vecModel
    model.save(dictModelFName['doc2vec'])

    return model


# create the updated doc2vec model
def updateDoctoVecModelClient(trainCorpus, doc2vecfName):
    # generate the model for the training document
    model = gensim.models.Doc2Vec.load(doc2vecfName)
    # build the vocab
    model.build_vocab(trainCorpus, update=True)
    # train the model
    model.train(trainCorpus, total_examples=model.corpus_count, epochs=model.epochs)
    # save the doc2vecModel
    model.save(dictModelFName['doc2vecUpdated'])


# update the doc2vec model that returns the aligned/intersected models
# from a list of gensim doc2vec models. Generalized from original two-way
# intersection as seen above. If 'words' is set (as list or set), then
# the vocabulary is intersected with this list as well.
# updated to word to vec from tangent's port https://gist.github.com/tangert/106822a0f56f8308db3f1d77be2c7942
# Code originally ported from HistWords
# <https://github.com/williamleif/histwords> by William Hamilton <wleif@stanford.edu>
def updateDoctoVecModelServer(currentDoc2VecName, latestDoc2VecName, words=None):
    # upload the models
    currDoc2Vec = gensim.models.Doc2Vec.load(dictModelFName[currentDoc2VecName])
    latestDoc2Vec = gensim.models.Doc2Vec.load(dictModelFName[latestDoc2VecName])

    # models = currentDoc2Vec and latestDoc2Vec model
    models = [currDoc2Vec, latestDoc2Vec]

    # Get the vocab for each model
    vocabs = [set(m.wv.vocab.keys()) for m in models]

    # Find the common vocabulary
    common_vocab = reduce((lambda vocab1, vocab2: vocab1 & vocab2), vocabs)
    if words: common_vocab &= set(words)

    # If no alignment necessary because vocab is identical...

    # This was generalized from:
    # if not vocab_m1-common_vocab and not vocab_m2-common_vocab and not vocab_m3-common_vocab:
    #   return (m1,m2,m3)
    if all(not vocab - common_vocab for vocab in vocabs):
        print("All identical!")
        return currDoc2Vec

    # Otherwise sort by frequency (summed for both)
    common_vocab = list(common_vocab)
    common_vocab.sort(key=lambda w: sum([m.wv.vocab[w].count for m in models]), reverse=True)

    # Then for current Model
    # Replace old vectors_norm array with new one (with common vocab)
    indices = [currDoc2Vec.wv.vocab[w].index for w in common_vocab]

    # old_arr = m.wv.vectors_norm
    old_arr = currDoc2Vec.wv.vectors
    # old_arr = np.linalg.norm(currDoc2Vec.wv.vectors, axis=1)

    print(old_arr)

    new_arr = np.array([old_arr[index] for index in indices])
    # m.wv.vectors_norm = m.wv.syn0 = new_arr
    currDoc2Vec.wv.vectors = currDoc2Vec.wv.syn0 = new_arr

    # Replace old vocab dictionary with new one (with common vocab)
    # and old index2word with new one
    currDoc2Vec.wv.index2word = common_vocab
    old_vocab = currDoc2Vec.wv.vocab
    new_vocab = {}
    for new_index, word in enumerate(common_vocab):
        old_vocab_obj = old_vocab[word]
        new_vocab[word] = gensim.models.word2vec.Vocab(index=new_index, count=old_vocab_obj.count)
    currDoc2Vec.wv.vocab = new_vocab

    # save the doc2vecModel
    currDoc2Vec.save(dictModelFName['doc2vec'])