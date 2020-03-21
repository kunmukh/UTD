#!/usr/bin/env python3.6

# Kunal Mukherjee
# 3/15/20
# Federated Learning of Encoders and word2vec
# federatedServer.py

# import statements
import socket
import sys
import ssl
import datetime

import smart_open
import gensim
import pickle
import os
import tqdm
from sklearn.model_selection import train_test_split
from keras.layers import Input, Dense
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras import regularizers
from keras.models import Model, load_model
from matplotlib import pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
import pprint
from sklearn.manifold import TSNE
# importing functools for reduce()
from functools import reduce

# Global constants
# the server listen addr and port
listen_addr = 'localhost'
listen_port = 10000
# server certificate and key
# openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout server.key -out server.crt
server_cert = 'certificates/server.crt'
server_key = 'certificates/server.key'
# client certificate
client_certs = 'certificates/client.crt'
# size of byte
byte_size = 1024
# dict of model files
dictModelFName = dict({'encoder': "models/model_seqs2.h5",
                       'doc2vec': "models/doc2vecModel.pickle",
                       'doc2vecUpdated': "models/doc2vecModelUpdated.pickle"})

# TODO: remove them and get real dataset
# training and testing dataset
lee_train_file = '../../data/adult_train.txt'
lee_test_file = '../../data/adult_test.txt'

# -----------------------------------------------


# utility to convert date to a desired format
# format the date in correct order
def getDate(date):

    format_date = date.replace("-", "_")
    year, month, date = format_date.split("_")

    if len(month) < 2:
        month = '0' + month
    if len(date) < 2:
        date = '0' + date
    if len(year) < 2:
        year = '0' + year

    return month + "_" + date + "_" + year

# -----------------------------------------------


# initialize a socket with ip and port
# return a ssl context and the socket
def initializeSocket(ip_addr, port):

    # create the ssl context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_cert_chain(certfile=server_cert, keyfile=server_key)
    context.load_verify_locations(cafile=client_certs)

    # create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = (ip_addr, port)
    print(sys.stderr, 'starting up on %s port %s' % server_address)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    return sock, context

# --------------------------------------------------


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


# update the doc2vec model that returns the aligned/intersected models
# from a list of gensim doc2vec models. Generalized from original two-way
# intersection as seen above. If 'words' is set (as list or set), then
# the vocabulary is intersected with this list as well.
# updated to word to vec from tangent's port https://gist.github.com/tangert/106822a0f56f8308db3f1d77be2c7942
# Code originally ported from HistWords
# <https://github.com/williamleif/histwords> by William Hamilton <wleif@stanford.edu>
def updateDoctoVecModel(currentDoc2VecName, latestDoc2VecName, words=None):
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

    checkpointer = ModelCheckpoint(filepath=dictModelFName['encoder'],
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
def createEncoderModel(train_file):

    # try to load the doc2vec model
    if os.path.isfile(dictModelFName['doc2vec']):
        pass
    else:
        # get the training and testing data
        train_corpus = dataProcessing(train_file, 'train')
        # generate the doc2vec model and get the feature for the training
        doc2vecModel = createDoctoVecModel(train_corpus)

        if os.path.isfile(dictModelFName['encoder']):
            pass
        else:
            # get the feature vector
            feature_vec_train = doc2vecModel[doc2vecModel.wv.vocab]
            # encode the feature of the training document
            autoEncoder(feature_vec_train)

            # save the accuracy plot
            plt.savefig('img/accuracyPlot_'+getDate(str(datetime.datetime.now().date()))+'.png', dpi=100)
            plt.clf()


# update the encoder model based on the provided doc2vec model
def updateEncoderModel(doc2vecName):
    try:
        doc2vecModel = gensim.models.Doc2Vec.load(dictModelFName[doc2vecName])

        # use the updated doc2vec to create the new encoder
        # get the feature vector
        feature_vec_train = doc2vecModel[doc2vecModel.wv.vocab]
        # encode the feature of the training document
        autoEncoder(feature_vec_train)

        # save the accuracy plot
        plt.savefig('img/accuracyPlot_' + getDate(str(datetime.datetime.now().date())) + '.png', dpi=100)
        plt.clf()

    except:
        print("Need to create doc2vec model first")

# --------------------------------------------------


# transfer the file given the connection
def fileTransfer(modelName, socket):
    # get the model file name
    fileName = dictModelFName[modelName]
    fileSize = os.path.getsize(fileName)

    SEPARATOR = "<SEPARATOR>"

    # send the filename and filesize
    socket.send(f"{fileName}{SEPARATOR}{fileSize}".encode())

    # start sending the file
    progress = tqdm.tqdm(range(fileSize), f"Sending {fileName}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(fileName, "rb") as f:
        for _ in progress:
            # read the bytes from the file
            bytes_read = f.read(byte_size)
            if not bytes_read:
                # file transmitting is done
                break
            # use sendall to assure transimission in
            # busy networks
            socket.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))


# file reception protocol
def fileReception(connection):
    SEPARATOR = "<SEPARATOR>"
    while True:
        # receive the file infos
        # receive using client socket, not server socket
        received = connection.recv(byte_size).decode()

        if not received:
            break

        print(received)
        filename, filesize = received.split(SEPARATOR)

        # remove absolute path if there is
        filename = 'models/' + os.path.basename(filename)
        # convert to integer
        filesize = int(filesize)

        # start receiving the file from the socket
        # and writing to the file stream
        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "wb") as f:
            for _ in progress:
                # read 1024 bytes from the socket (receive)
                bytes_read = connection.recv(byte_size)
                if not bytes_read:
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))

# --------------------------------------------------


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
    plt.savefig('img/TSNEPlot_' + getDate(str(datetime.datetime.now().date())) + '.png', dpi=100)
    plt.clf()
# --------------------------------------------------

def main():
    '''updateDoctoVecModel('doc2vec', 'doc2vecUpdated')
    # test the model
    testdoc2vecModel('doc2vec', lee_test_file)
    exit()'''
    # create the encoder model
    createEncoderModel(lee_train_file)

    # initialize a socket with ip and port
    sock, sslContext = initializeSocket(listen_addr, listen_port)

    while True:
        # Wait for a connection
        print(sys.stderr, 'waiting for a connection')
        newSocket, client_address = sock.accept()

        # ssl checking the client certificate
        try:
            connection = sslContext.wrap_socket(newSocket, server_side=True)
            print("SSL established. Peer: {}".format(connection.getpeercert()))

            try:
                print(sys.stderr, 'connection from', client_address)

                # Receive the data and check if it is the first initial message or not
                while True:
                    data = connection.recv(byte_size)
                    print(sys.stderr, 'received "%s"' % data)

                    if data:
                        if "Requesting" in str(data):
                            # the first transmission
                            if "encoder" in str(data):
                                print(sys.stderr, 'Connection from client:', client_address)
                                print(sys.stderr, 'sending encoder model to the client')

                                fileTransfer('encoder', connection)

                                print(sys.stderr, 'Sending complete. Closing connection to:', client_address)
                                break
                            elif "doc2vec" in str(data):
                                print(sys.stderr, 'Connection from client:', client_address)
                                print(sys.stderr, 'sending doc2vec model to the client')

                                fileTransfer('doc2vec', connection)

                                print(sys.stderr, 'Sending complete. Closing connection to:', client_address)
                                break
                        if "Sending" in str(data):
                            print(sys.stderr, 'Connection from client:', client_address)
                            print(sys.stderr, 'receiving doc2vec model from the client')

                            # receive the file
                            fileReception(connection)

                            print(sys.stderr, 'Reception complete. Closing connection to:', client_address)

                            # TODO: Update the doc2vec model
                            updateDoctoVecModel('doc2vec', 'doc2vecUpdated')
                            # test the model
                            testdoc2vecModel('doc2vecUpdated', lee_test_file)

                            # update the encoder model with the Updated doc2vec model
                            updateEncoderModel('doc2vecUpdated')
                            break

                    else:
                        print(sys.stderr, 'no more data from', client_address)
                        break

            finally:
                # clean up the connection
                connection.close()

        except ssl.SSLError:
            print("SSL Handshake Failed")





if __name__ == '__main__':
    main()

