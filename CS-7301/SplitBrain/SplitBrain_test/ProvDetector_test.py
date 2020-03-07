#!/usr/bin/python3

# Kunal Mukherjee
# Gensim lib (PV-DM) + LOF
# 2/9/2020


from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
from sklearn.neighbors import LocalOutlierFactor
import smart_open
import gensim
import numpy as np
import pandas as pd
import pprint


# Set file names for train and test data
#lee_train_file = 'data/lee_train.txt'
#lee_test_file = 'data/lee_test.txt'

lee_train_file = 'data/adult_train.txt'
lee_test_file = 'data/adult_test.txt'
# lee_test_file = 'data/bad_test.txt'
# lee_test_file = 'data/child_test.txt'


def read_corpus(fname, tokens_only=False):
    with smart_open.open(fname, encoding="iso-8859-1") as f:
        for i, line in enumerate(f):
            tokens = gensim.utils.simple_preprocess(line)
            if tokens_only:
                yield tokens
            else:
                # For training data, add tags
                yield gensim.models.doc2vec.TaggedDocument(tokens, [i])


def main():
    train_corpus = list(read_corpus(lee_train_file))
    test_corpus = list(read_corpus(lee_test_file, tokens_only=True))

    model = gensim.models.doc2vec.Doc2Vec(min_count=2, epochs=40)
    # print(pd.DataFrame(data=train_corpus))
    model.build_vocab(train_corpus)

    # summarize the loaded model
    # print("model:", model)

    # get the words form the dict
    # words = list(model.wv.vocab)
    # print("Words: ", words)

    # access feature vector for one word
    # print("Vec for 'sentence'", model['sentence'])

    # access count of feature vector for one word
    # print(model.wv.vocab['sentence'].count)

    # get the feature vector from the training data set
    feature_vec_train = model[model.wv.vocab]
    # pprint.pprint(model.wv.vocab)
    # print(" Feature Training Vector: \n", pd.DataFrame(data=feature_vec_train))

    # Shape of the training corpus feature vectors
    print("Vec", feature_vec_train.shape)

    # Testing the model

    # extract the feature vector for each corpus in the test corpus
    feature_vec_test = []
    for i, corpus in enumerate(test_corpus):
        feature_vec_test.extend([model.infer_vector(corpus)])

    # print(feature_vec_test)
    print(" Feature Test Vector: \n", pd.DataFrame(data=feature_vec_test))
    # print("Test Vec", np.asarray(feature_vec_test).shape)

    # Novelty detection with Local Outlier Factor (LOF)
    lof = LocalOutlierFactor(n_neighbors=40, contamination=0.1, novelty=True)
    lof.fit(feature_vec_train)

    # Novelty detecting on the feature vector of the testing corpus
    y_pred_test = lof.predict(feature_vec_test)

    print(pd.DataFrame(data=y_pred_test))

    # get the inlier and the outlier
    feature_vec_test_inlier_indices = y_pred_test > 0
    feature_vec_test_outlier_indices = y_pred_test < 0

    feature_vec_test_inlier = np.asarray(feature_vec_test)[feature_vec_test_inlier_indices]
    feature_vec_test_outlier = np.asarray(feature_vec_test)[feature_vec_test_outlier_indices]

    print("Inlier or Outlier:")
    print("% of Inlier :", len(feature_vec_test_inlier) / len(y_pred_test))
    print("% of Outlier:", len(feature_vec_test_outlier) / len(y_pred_test))

    #Plot using TSNE
    plt.subplot(122)
    plt.xlabel("T-SNE")
    tsne = TSNE(n_components=2, perplexity=50, n_iter=300)

    # plotting Training feature vector using TSNE
    tsne_results_train = tsne.fit_transform(feature_vec_train)
    plt.scatter(tsne_results_train[:, 0], tsne_results_train[:, 1], c='black')

    # in-lier feature vector
    tsne_results_test = tsne.fit_transform(feature_vec_test_inlier)
    plt.scatter(tsne_results_test[:, 0], tsne_results_test[:, 1], c='blue')

    # out-lier feature vector
    if (len(feature_vec_test_outlier) > 2):
        tsne_results_test = tsne.fit_transform(feature_vec_test_outlier)
        plt.scatter(tsne_results_test[:, 0], tsne_results_test[:, 1], c='red')

    # Plot using PCA
    plt.subplot(121)
    plt.xlabel("PCA")
    pca = PCA(n_components=2)

    # plotting Training feature vector using PCA
    result = pca.fit_transform(feature_vec_train)
    # create a scatter plot of the projection
    plt.scatter(result[:, 0], result[:, 1], c='black')

    # in-lier feature vector
    result = pca.fit_transform(feature_vec_test_inlier)
    plt.scatter(result[:, 0], result[:, 1], c='blue')

    # out-lier feature vector
    if (len(feature_vec_test_outlier) > 2):
        result = pca.fit_transform(feature_vec_test_outlier)
        plt.scatter(result[:, 0], result[:, 1], c='red')

    plt.show()
    

if __name__ == '__main__':
    main()
    
''' # define training data
    sentences = [['this', 'is', 'the', 'first', 'sentence', 'for', 'word2vec'],
                 ['this', 'is', 'the', 'second', 'sentence'],
                 ['yet', 'another', 'sentence'],
                 ['one', 'more', 'sentence'],
                 ['and', 'the', 'final', 'sentence']]
    # train model
    model = Word2Vec(sentences, min_count=1)'''

'''# PCA
    plt.subplot(121)
    plt.xlabel("PCA")
    pca = PCA(n_components=2)
    result = pca.fit_transform(feature_vec)
    # create a scatter plot of the projection
    plt.scatter(result[:, 0], result[:, 1])
    words = list(model.wv.vocab)
    # for i, word in enumerate(words):
        # plt.annotate(word, xy=(result[i, 0], result[i, 1]))'''