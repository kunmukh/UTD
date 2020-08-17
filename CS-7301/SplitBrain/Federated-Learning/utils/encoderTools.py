#!/usr/bin/env python3.6

# Kunal Mukherjee
# 4/3/20
# Federated Learning of Encoders and word2vec

import numpy as np
import gensim
import os
import datetime
from sklearn.model_selection import train_test_split
from keras.layers import Input, Dense
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras import regularizers
from keras.models import Model, load_model
from matplotlib import pyplot as plt

from utils import dateFormat
from utils import doc2vecTools
from utils import globalConst


# create the auto-encoder
def autoEncoder(feature_vec_train):
    # NORMALIZE THE DATA AND BUILD AN AUTOENCODER

    # normalize the feature
    # scaler = MinMaxScaler()
    # scaled_seqs = scaler.fit_transform(feature_vec_train)

    # no need to scale for feature vec in doc2vec
    # divide the data into train and test
    X_train, X_test = train_test_split(feature_vec_train, test_size = 0.20)

    # SETTING UP THE AUTO-ENCODER
    # TODO: test this hyper parameters
    input_dim = X_train.shape[1]  # features
    encoding_dim = input_dim
    hidden_dim = int(encoding_dim / 2)

    nb_epoch = 30
    batch_size = 128
    learning_rate = 0.1

    input_layer = Input(shape=(input_dim,))

    encoder = Dense(encoding_dim, activation="tanh",
                    activity_regularizer=regularizers.l1(10e-5))(input_layer)
    encoder = Dense(hidden_dim, activation="relu")(encoder)
    decoder = Dense(encoding_dim, activation='relu')(encoder)
    decoder = Dense(input_dim, activation='tanh')(decoder)

    # FIT THE MODEL

    autoencoder = Model(inputs=input_layer, outputs=decoder)

    autoencoder.compile(optimizer='adam',
                        loss='mean_squared_error',
                        metrics=['accuracy'])

    checkpointer = ModelCheckpoint(filepath=globalConst.dictFName['encoder'],
                                   verbose=0,
                                   save_best_only=True)

    tensorboard = TensorBoard(log_dir='./logs',
                              histogram_freq=0,
                              write_graph=True,
                              write_images=True)

    history = autoencoder.fit(X_train, X_train,
                              epochs=nb_epoch,
                              batch_size=batch_size,
                              shuffle=True,
                              validation_data=(X_test, X_test),
                              verbose=1,
                              callbacks=[checkpointer, tensorboard]).history
    # Print the minimum loss
    print('\n' + f'Min Loss:{np.min(history["loss"])}' + '\n')

    # plot the loss v epocs graph
    plt.plot(history['loss'])
    plt.plot(history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper right')


# check for the dependencies for the encoder model
def createEncoderModel(train_data_file_path):

    # try to load the doc2vec model
    if os.path.isfile(globalConst.dictFName['doc2vec']):
        pass
    else:
        # get the training and testing data
        # train_corpus = doc2vecTools.dataProcessing(train_data_file_path, 'train')
        train_corpus = doc2vecTools.dataProcessingCSV(train_data_file_path)

        # generate the doc2vec model and get the feature for the training
        # doc2vecModel = doc2vecTools.createDoctoVecModel(train_corpus)
        doc2vec_tr = doc2vecTools.Doc2VecTransformer()
        doc2vec_tr.fit(train_corpus)

        if os.path.isfile(globalConst.dictFName['encoder']):
            pass
        else:
            # get the feature vector
            # feature_vec_train = doc2vecModel[doc2vecModel.wv.vocab]
            feature_vec_train = doc2vec_tr.transform(train_corpus)

            # encode the feature of the training document
            autoEncoder(feature_vec_train)

            # save the accuracy plot
            plt.savefig('img/accuracyPlot_'+ dateFormat.getDate(str(datetime.datetime.now().date()))+'.png', dpi=100)
            plt.clf()


# update the encoder model based on the provided doc2vec model
def updateEncoderModel(doc2vecName, train_data_file_path):
    try:
        '''doc2vecModel = gensim.models.Doc2Vec.load(globalConst.dictFName[doc2vecName])

        # use the updated doc2vec to create the new encoder
        # get the feature vector
        feature_vec_train = doc2vecModel[doc2vecModel.wv.vocab]
        # encode the feature of the training document
        autoEncoder(feature_vec_train)'''

        # update the encoder model with the training data
        train_corpus = doc2vecTools.dataProcessingCSV(train_data_file_path)
        doc2vec_tr = doc2vecTools.Doc2VecTransformer(
            model=gensim.models.Doc2Vec.load(globalConst.dictFName[doc2vecName]))
        feature_vec_train = doc2vec_tr.transform(train_corpus)

        # encode the feature of the training document
        autoEncoder(feature_vec_train)

        # save the accuracy plot
        plt.savefig('img/accuracyPlot_' + dateFormat.getDate(str(datetime.datetime.now().date())) + '.png', dpi=100)
        plt.clf()

    except:
        print("Need to create doc2vec model first")