#!/usr/bin/env python3.6

# Kunal Mukherjee
# 4/3/20
# Testing the encoder models

# import statements
import gensim
from utils import doc2vecTools
from keras.models import Model, load_model
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# training and testing dataset
lee_train_file = '../../data/lee_train.txt'
lee_test_file = '../../data/lee_test.txt'


def main():
    # load the doc2vec model for server
    serverDoc2vecModel = gensim.models.Doc2Vec.load("../server/models/doc2vecModel.pickle")
    '''serverDoc2vecUpdateModel = gensim.models.Doc2Vec.load("../server/models/doc2vecModelUpdated.pickle")'''

    # load the autoencoder model for server
    '''serverAutoencoder = load_model("../server/models/model_seqs2.h5")'''

    '''doc2vecTools.testdoc2vecModel(serverDoc2vecModel, lee_test_file,
                                  True, 'serverDoc2vecModel', serverAutoencoder)
    doc2vecTools.testdoc2vecModel(serverDoc2vecUpdateModel, lee_test_file,
                                  True, 'serverDoc2vecUpdateModel', serverAutoencoder)'''

    # load the doc2vec model for client
    clientDoc2vecModel = gensim.models.Doc2Vec.load("../client/models/doc2vecModel.pickle")
    clientDoc2vecUpdateModel = gensim.models.Doc2Vec.load("../client/models/doc2vecModelUpdated.pickle")

    # load the autoencoder model for client
    clientAutoencoder = load_model("../client/models/model_seqs2.h5")

    '''# test the doc2vec models
    doc2vecTools.testdoc2vecModel(clientDoc2vecModel, lee_test_file, True,
                                  'clientDoc2vecModel', clientAutoencoder)
    doc2vecTools.testdoc2vecModel(clientDoc2vecUpdateModel, lee_test_file,
                                  True, 'clientDoc2vecUpdateModel', clientAutoencoder)'''

    # https://rutumulkar.com/blog/2015/word2vec/
    # load the word vectors
    vectorClient = clientDoc2vecModel.wv.vectors
    vectorUpdateClient = clientDoc2vecUpdateModel.wv.vectors
    vectorServer = serverDoc2vecModel.wv.vectors

    # print the word vectors
    print('VectorClient\n', pd.DataFrame(vectorClient))
    print('VectorUpdateClient\n', pd.DataFrame(vectorUpdateClient))
    print('VectorServer\n', pd.DataFrame(vectorServer))

    sum_simi = 0
    for i in range(vectorClient.shape[0]):
        sum_simi += cosine_similarity(vectorClient[i].reshape(1, 100), vectorServer[i].reshape(1, 100))
        '''print(i, "Similarity between vectors:\n", cosine_similarity(vectorClient[i].reshape(1, 100),
                                                                    vectorServer[i].reshape(1, 100)))'''
    print("Total similarity between client and server updated vector:", sum_simi / vectorClient.shape[0], '\n')

    # load the test corpus
    testCorpus1 = doc2vecTools.dataProcessing("evalData/test.data", 'test')
    testCorpus2 = doc2vecTools.dataProcessing("evalData/test2.data", 'test')

    print('test corpus1\n', pd.DataFrame(testCorpus1))
    print('test corpus2\n', pd.DataFrame(testCorpus2))

    # get the feature vector for clientDoc2vec model
    featureVec1 = doc2vecTools.DoctoVecFeatureInfer(clientDoc2vecModel, testCorpus1)
    featureVec2 = doc2vecTools.DoctoVecFeatureInfer(clientDoc2vecModel, testCorpus2)

    # find the similarity between the vectors
    print('feature vector similarity clientDoc2vec\n', cosine_similarity(featureVec1, featureVec2))

    # get the feature vector for clientDoc2vecUpdated model
    featureVec1 = doc2vecTools.DoctoVecFeatureInfer(clientDoc2vecUpdateModel, testCorpus1)
    featureVec2 = doc2vecTools.DoctoVecFeatureInfer(clientDoc2vecUpdateModel, testCorpus2)

    print('feature vector similarity clientDoc2vecUpdate\n', cosine_similarity(featureVec1, featureVec2))

    '''featureVec1 = doc2vecTools.DoctoVecFeatureInfer(serverDoc2vecModel, testCorpus1)
    featureVec2 = doc2vecTools.DoctoVecFeatureInfer(serverDoc2vecModel, testCorpus2)

    print('feature vector similarity serverDoc2vecModel', cosine_similarity(featureVec1, featureVec2))'''


if __name__ == '__main__':
    main()