#!/usr/bin/env python3.6

# Kunal Mukherjee
# 4/3/20
# Federated Learning of Encoders and word2vec

import numpy as np
import pandas as pd
import gensim
from gensim import utils
import gensim.parsing.preprocessing as gsp
from keras.models import Model, load_model
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
import seaborn as sns
import datetime
import smart_open
from functools import reduce
from collections import Counter
from itertools import islice
from sklearn.base import BaseEstimator
from sklearn import utils as skl_utils
from tqdm import tqdm
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


from utils import dateFormat
from utils import globalConst


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


# clean the data
def clean_text(s):
    # define the filter
    filters = [
        gsp.strip_tags,
        gsp.strip_punctuation,
        gsp.strip_multiple_whitespaces,
        gsp.strip_numeric,
        gsp.remove_stopwords,
        gsp.strip_short,
        gsp.stem_text
    ]
    # put all the test to lower case
    s = s.lower()
    # change it to unicode
    s = utils.to_unicode(s)
    # filter the text out
    for f in filters:
        s = f(s)
    return s


# generate the training corpus with CSV
def dataProcessingCSV(filePath):
    # load the csv file
    data_df = pd.read_csv(filePath, index_col=False, header=0)
    # select the only required columns
    dataHeader = ['Rating', 'Plot']
    processed_df = data_df[dataHeader]
    # process the data on those columns
    processed_df['Plot'] = processed_df['Plot'].map(lambda x: clean_text(x))
    processed_df = processed_df.rename(columns={'Plot': 'Data'})

    '''# plot the top most frequently used words
    findCommonWords(processed_df, True, 10)
    # plot the top least frequently used words
    findCommonWords(processed_df, False, 10)
    plt.show()'''

    return processed_df


# plot the top n most/least frequently used words
def findCommonWords(data_df, common, n, doPlot=False):
    # most frequent 50 words
    aggregate_counter = Counter()
    for row_index, row in data_df.iterrows():
        c = Counter(row['Data'].split())
        aggregate_counter += c

    if common:
        common_words = [word[0] for word in aggregate_counter.most_common(n)]
        common_words_counts = [word[1] for word in aggregate_counter.most_common(n)]

        # plot the most common 50 words
        if doPlot:
            barplot(words=common_words, words_counts=common_words_counts,
                    title='Most Frequent Words used in movie plots')
        else:
            return common_words, Counter(aggregate_counter.most_common(n))
    else:
        # least common 50 words
        all_word_counts = sorted(aggregate_counter.items(), key=key_word_counter)
        uncommon_words = [word[0] for word in islice(all_word_counts, n)]
        uncommon_words_counts = [word[1] for word in islice(all_word_counts, n)]
        uncommon_word_count_items = [word for word in islice(all_word_counts, 300000)]

        # plot the least common 50 words
        if doPlot:
            barplot(words=uncommon_words, words_counts=uncommon_words_counts,
                    title='Least Frequent Words used in movie plots')
        else:
            return uncommon_words,  Counter(dict(uncommon_word_count_items))


def key_word_counter(tupple):
    return tupple[1]


# plot the most/least common words
def barplot(words, words_counts, title):
    fig = plt.figure(figsize=(18,6))
    bar_plot = sns.barplot(x=words, y=words_counts)
    for item in bar_plot.get_xticklabels():
        item.set_rotation(90)
    plt.title(title)


# utility for testing doc2vec model
# infer the feature for the test_corpus from the doc2vec model
def DoctoVecFeatureInfer(doc2vecmodel, test_corpus):
    num_features = 100

    # extract the feature vector for each corpus in the test corpus
    feature_vec_test = np.empty((0, num_features))
    for i, corpus in enumerate(test_corpus):
        feature_vec_test = np.append(feature_vec_test, [doc2vecmodel.infer_vector(corpus)], axis=0)

    # print(" Feature Test Vector: \n", pd.DataFrame(data=feature_vec_test).head())
    # print("Test Vec", np.asarray(feature_vec_test).shape)

    # normalize it
    # feature_vec_test = MinMaxScaler().fit_transform(feature_vec_test)
    # print(feature_vec_test)

    return feature_vec_test


# predict the in-lier and out-lier
def prediction(doc2vecmodel, test_corpus, feature_vec_test, encoderModel=None):
    # PREDICTION STEP
    if encoderModel is not None:
        autoencoder = encoderModel
    else:
        autoencoder = load_model(globalConst.dictFName['encoder'])

    '''# Testing the model
    feature_vec_test = DoctoVecFeatureInfer(doc2vecmodel, test_corpus)

    # combine test and train feature vec
    feature_vec = np.concatenate((feature_vec_train, feature_vec_test), axis=0)

    # predict it
    predicted = autoencoder.predict(feature_vec)    

    return feature_vec, predicted'''

    # predict it
    predicted = autoencoder.predict(feature_vec_test)

    return feature_vec_test, predicted


# use mean sq. error to calculate anomaly
def meanSqError (feature_vec, predicted_vec):
    # get the error term
    mse = np.mean(np.power(feature_vec - predicted_vec, 2), axis=1)

    # now add them to our data frame
    seqs_ds = pd.DataFrame(data={'Doc #': [i for i in range(0, feature_vec.shape[0])]})

    seqs_ds['MSE'] = mse

    print(seqs_ds)

    # getting the threshold
    # TODO: test threshold hyper parameters org:0.9997
    mse_threshold = np.quantile(seqs_ds['MSE'], 0.9900)
    print('\n' + f'MSE 0.9997 threshold:{mse_threshold}' + '\n')

    # updating the MSE Outlier
    seqs_ds['MSE_Outlier'] = 0
    seqs_ds.loc[seqs_ds['MSE'] > mse_threshold, 'MSE_Outlier'] = 1

    # print(seqs_ds)
    # print(seqs_ds.loc[seqs_ds['MSE_Outlier'] == 1])

    print('\n' + f"Num of MSE outlier:{seqs_ds['MSE_Outlier'].sum()}" + '\n')

    feature_vec_inlier_indices  = seqs_ds['MSE_Outlier'] <= 0
    feature_vec_outlier_indices = seqs_ds['MSE_Outlier'] > 0

    feature_vec_inlier = np.asarray(feature_vec)[feature_vec_inlier_indices]
    feature_vec_outlier = np.asarray(feature_vec)[feature_vec_outlier_indices]

    '''print("Inlier or Outlier:")
    print("% of Inlier :", len(feature_vec_inlier) / len(seqs_ds['MSE_Outlier']))
    print("% of Outlier:", len(feature_vec_outlier) / len(seqs_ds['MSE_Outlier']))'''

    feature_vec_inlier_ind = np.asarray(seqs_ds.loc[seqs_ds['MSE_Outlier'] == 0, 'Doc #'])
    feature_vec_outlier_ind = np.asarray(seqs_ds.loc[seqs_ds['MSE_Outlier'] == 1, 'Doc #'])

    '''return feature_vec_inlier, feature_vec_outlier'''
    return feature_vec_inlier, feature_vec_inlier_ind, \
           feature_vec_outlier, feature_vec_outlier_ind


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
def testdoc2vecModel(modelName, testFilePath,
                     model=False, modelNameExplicite=None, encoderModel=None):

    if model:
        doc2vecModel = modelName
    else:
        doc2vecModel = gensim.models.Doc2Vec.load(globalConst.dictFName[modelName])

    # get the test corpus
    test_corpus = dataProcessingCSV(testFilePath)
    # get the model
    doc2vec_tr = Doc2VecTransformer(
        model=gensim.models.Doc2Vec.load(globalConst.dictFName[modelName]))

    # get the feature vector
    feature_vec_test = doc2vec_tr.transform(test_corpus)

    '''# get the test corpus
    test_corpus = dataProcessing(testFilePath, 'test')

    # get the feature vector
    feature_vec = doc2vecModel[doc2vecModel.wv.vocab]'''

    # get the prediction of the inlier and outlier from the test_corpus
    if encoderModel is not None:
        updated_feature_vec, pred = prediction(doc2vecModel, test_corpus, feature_vec_test, encoderModel)
    else:
        updated_feature_vec, pred = prediction(doc2vecModel, test_corpus, feature_vec_test)

    # get the meanSqError from the feature_vec_test, predicition_vec, feature_vec_train
    feature_vec_inlier, feature_vec_inlier_ind, feature_vec_outlier, feature_vec_outlier_ind =\
        meanSqError(updated_feature_vec, pred)

    print(test_corpus.iloc[feature_vec_outlier_ind])
    neg_pred_y = np.asarray(test_corpus.iloc[feature_vec_outlier_ind].loc[:, 'Rating'])
    y_test = np.zeros(shape=(1, len(feature_vec_outlier_ind))).tolist()[0]
    print('Accuracy for outlier: ', accuracy_score(y_test, neg_pred_y))

    pos_pred_y = np.asarray(test_corpus.iloc[feature_vec_inlier_ind].loc[:, 'Rating'])
    y_test = np.ones(shape=(1, len(feature_vec_inlier_ind))).tolist()[0]
    print('Accuracy for inlier: ', accuracy_score(y_test, pos_pred_y))

    '''# find the common words
    find_intersected_words(test_corpus, feature_vec_outlier_ind, True, True)
    # find the uncommon words
    find_intersected_words(test_corpus, feature_vec_outlier_ind, False, True)'''

    '''# plot the TSNE
    plotTSNE(feature_vec_test, feature_vec_inlier, feature_vec_outlier)

    # save the accuracy plot
    if model:
        plt.savefig('img/TSNEPlot_' + dateFormat.getDate(str(datetime.datetime.now().date())) + modelNameExplicite
                    + '.png', dpi=100)
    else:
        plt.savefig('img/TSNEPlot_' + dateFormat.getDate(str(datetime.datetime.now().date())) + modelName +'.png',
                    dpi=100)
    plt.clf()'''


# whether there is an intersection between ‘all processed words of most unique movie’ and
# ‘very frequent words across all movies’
# https://medium.com/datadriveninvestor/unsupervised-outlier-detection-in-text-corpus-using-deep-learning-41d4284a04c8
def find_intersected_words(test_corpus, feature_vec_outlier_ind, common=True, plot=False):

    # get the unique data
    most_unique_data = test_corpus.iloc[feature_vec_outlier_ind[0]].loc['Data']
    # get the dict of the words and counter
    most_unique_words_counter = Counter(gsp.preprocess_string(most_unique_data))

    if common:
        # get the dict of the most common words and counter from the test corpus
        test_word, test_word_counter = findCommonWords(test_corpus, True, 50)
    else:
        # get the dict of the most uncommon words and counter from the test corpus
        test_word, test_word_counter = findCommonWords(test_corpus, False, 50)

    # get the dict of the intersected words and counter from the test corpus
    intersected_word_counter = test_word_counter & most_unique_words_counter

    intersected_words = [word[0] for word in intersected_word_counter.items()]
    intersected_word_counts = [word[1] for word in intersected_word_counter.items()]

    '''# print the common words and their count
    print(intersected_word_counter)
    print(intersected_words)
    print(intersected_word_counts)'''

    # plot the words
    if plot and intersected_words != []:
        barplot(words=intersected_words, words_counts=intersected_word_counts,
                title='Few Common words between all words of most unique movie & least frequent words in all movies')
        if common:
            plt.savefig('img/Words_' + dateFormat.getDate(str(datetime.datetime.now().date())) + "common"
                        + '.png', dpi=100)
        else:
            plt.savefig('img/Words_' + dateFormat.getDate(str(datetime.datetime.now().date())) + "uncommon"
                        + '.png', dpi=100)
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
    model.save(globalConst.dictFName['doc2vec'])

    return model


# create the updated doc2vec model
def updateDoctoVecModelClient(trainCorpus, doc2vecfpath):
    # generate the model for the training document
    # model = gensim.models.Doc2Vec.load(doc2vecfName)

    # load the model
    doc2vec_tr = Doc2VecTransformer(
        model=gensim.models.Doc2Vec.load(doc2vecfpath))

    # build the vocab
    # model.build_vocab(trainCorpus, update=True)
    tagged_tr = [gensim.models.doc2vec.TaggedDocument(str(row['Data']).split(),
                                                     [index]) for index, row in trainCorpus.iterrows()]

    doc2vec_tr.getModel().build_vocab(tagged_tr, update=True)
    # train the model
    # model.train(trainCorpus, total_examples=model.corpus_count, epochs=model.epochs)
    doc2vec_tr.fit(trainCorpus)
    # save the doc2vecModel
    # model.save(globalConst.dictFName['doc2vecUpdated'])
    doc2vec_tr.getModel().save(globalConst.dictFName['doc2vecUpdated'])


# update the doc2vec server model of the server by using data
def updateDoctoVecModelServer(trainCorpus, doc2vecfpath):

    # load the model
    doc2vec_tr = Doc2VecTransformer(
        model=gensim.models.Doc2Vec.load(doc2vecfpath))

    # build the vocab
    tagged_tr = [gensim.models.doc2vec.TaggedDocument(str(row['Data']).split(),
                                                      [index]) for index, row in trainCorpus.iterrows()]

    doc2vec_tr.getModel().build_vocab(tagged_tr, update=True)
    # train the model
    doc2vec_tr.fit(trainCorpus)
    # save the doc2vecModel
    doc2vec_tr.getModel().save(globalConst.dictFName['doc2vecUpdated'])

# server model joining
'''# update the doc2vec model that returns the aligned/intersected models
# from a list of gensim doc2vec models. Generalized from original two-way
# intersection as seen above. If 'words' is set (as list or set), then
# the vocabulary is intersected with this list as well.
# updated to word to vec from tangent's port https://gist.github.com/tangert/106822a0f56f8308db3f1d77be2c7942
# Code originally ported from HistWords
# <https://github.com/williamleif/histwords> by William Hamilton <wleif@stanford.edu>
def updateDoctoVecModelServer(currentDoc2VecName, latestDoc2VecName, words=None):
    # upload the models
    currDoc2Vec = gensim.models.Doc2Vec.load(globalConst.dictModelFName[currentDoc2VecName])
    latestDoc2Vec = gensim.models.Doc2Vec.load(globalConst.dictModelFName[latestDoc2VecName])

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
    currDoc2Vec.syn0_lockf = np.zeros(np.shape(currDoc2Vec.syn0_lockf))

    # save the doc2vecModel
    currDoc2Vec.save(globalConst.dictModelFName['doc2vec'])'''


# a doc2vec transformer
class Doc2VecTransformer(BaseEstimator):

    # TODO: play with the hyperparameters
    def __init__(self, vector_size=100, learning_rate=0.02, epochs=20, model=None): # epochs = 20
        self.learning_rate = learning_rate
        self.epochs = epochs
        self._model = model
        self.vector_size = vector_size

    def fit(self, df_x, df_y=None):
        tagged_x = [gensim.models.doc2vec.TaggedDocument(str(row['Data']).split(),
                                                         [index]) for index, row in df_x.iterrows()]
        model = gensim.models.doc2vec.Doc2Vec(documents=tagged_x,
                                              vector_size=self.vector_size)

        for epoch in range(self.epochs):
            model.train(skl_utils.shuffle([x for x in tqdm(tagged_x)]), total_examples=len(tagged_x), epochs=1)
            model.alpha -= self.learning_rate
            model.min_alpha = model.alpha

        self._model = model

        # save the doc2vecModel
        model.save(globalConst.dictFName['doc2vec'])

        return self

    def transform(self, df_x):
        return np.asmatrix(np.array([self._model.infer_vector(str(row['Data']).split())
                                     for index, row in df_x.iterrows()]))

    def getModel(self):
        return self._model

    def updateModel(self, model):
        self._model = model