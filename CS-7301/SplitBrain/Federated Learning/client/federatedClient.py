#!/usr/bin/env python3.6

# Kunal Mukherjee
# 3/15/20
# Federated Learning of Encoders and word2vec
# federatedClient.py

# import statements
import socket
import sys
import ssl
import pickle
import os
import tqdm
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
import smart_open
import gensim
import numpy as np
import pandas as pd
from keras.models import Model, load_model
import datetime

# Global constants
# Server information
host_addr = 'localhost'
host_port = 10000
server_sni_hostname = 'fedserver.com'
# server certificate
# openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout client.key -out client.crt
server_cert = 'certificates/server.crt'
# client certificate and key
client_cert = 'certificates/client.crt'
client_key = 'certificates/client.key'
# size of byte
byte_size = 1024
# receive 4096 bytes each time
SEPARATOR = "<SEPARATOR>"
# dict of model files
dictModelFName = dict({'encoder': "models/model_seqs2.h5",
                       'doc2vec': "models/doc2vecModel.pickle",
                       'doc2vecUpdated': "models/doc2vecModelUpdated.pickle"})
# number of models
models = ['encoder', 'doc2vec']

# TODO: remove them and get real dataset
# training and testing dataset
lee_train_file = '../../data/adult_train.txt'
lee_test_file = '../../data/adult_test.txt'

# --------------------------------------------------


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
# --------------------------------------------------


# initialize the connection with the server
# return the connection socket
def initializeConnection(server_ip, server_port):
    # Load the ssl context
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
    context.load_cert_chain(certfile=client_cert, keyfile=client_key)

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # ssl context wrap
    connection = context.wrap_socket(sock, server_side=False, server_hostname=server_sni_hostname)

    # Connect the socket to the port where the server is listening
    server_address = (server_ip, server_port)
    print(sys.stderr, 'connecting to %s port %s' % server_address)

    # if the connection can be made
    try:
        connection.connect(server_address)
        return sock, connection
    # the connection failed, close the socket and exit
    except ssl.SSLError:
        print("SSL Handshake Failed")
        sock.close()
        exit()
# --------------------------------------------------


# file reception protocol
def fileReception(connection):
    while True:
        # receive the file infos
        # receive using client socket, not server socket
        received = connection.recv(byte_size).decode()

        if not received:
            break

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
# --------------------------------------------------


# get the initial encoder and doc2vec model
def getInitialModels():
    # get the initial models: encoder and doc2vec
    for model in models:
        # create the connection the the server
        sock, connection = initializeConnection(host_addr, host_port)

        try:
            # Send the request to get encoder and doc2vec model
            message = 'Connection Requesting ' + model + ' model'
            print(sys.stderr, 'sending "%s"' % message)
            connection.sendall(message.encode('UTF-8'))

            # receive the file
            fileReception(connection)

        finally:
            print(sys.stderr, 'closing socket')
            sock.close()


# send the updated doc2vec model
def senddoc2vecUpdatedModel():
    # send the updated doc2vec model
    # create the connection the the server
    sock, connection = initializeConnection(host_addr, host_port)

    try:
        # Send the request to get encoder and doc2vec model
        message = 'Connection Sending doc2vec model'
        print(sys.stderr, 'sending "%s"' % message)
        connection.sendall(message.encode('UTF-8'))

        # receive the file
        fileTransfer('doc2vecUpdated', connection)

    finally:
        print(sys.stderr, 'closing socket')
        sock.close()
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
# --------------------------------------------------


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
    # load the model
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
# --------------------------------------------------


# create the updated doc2vec model
def updateDoctoVecModel(trainCorpus, doc2vecfName):
    # generate the model for the training document
    model = gensim.models.Doc2Vec.load(doc2vecfName)
    # build the vocab
    model.build_vocab(trainCorpus, update=True)
    # train the model
    model.train(trainCorpus, total_examples=model.corpus_count, epochs=model.epochs)
    # save the doc2vecModel
    model.save(dictModelFName['doc2vecUpdated'])
# --------------------------------------------------


def main():
    # get the initial encoder and doc2vec model
    getInitialModels()

    # do the prediction from the model data
    testdoc2vecModel('doc2vec', lee_test_file)

    # TODO: create the updated doc2vec model
    # the new training file
    updateDoctoVecModel(dataProcessing(lee_test_file, 'train'), dictModelFName['doc2vec'])

    # send the updated doc2vec model
    senddoc2vecUpdatedModel()


if __name__ == '__main__':
    main()