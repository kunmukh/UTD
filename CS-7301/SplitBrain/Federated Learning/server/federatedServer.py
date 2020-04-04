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

# utilities
from utils import dateFormat
from utils import network
from utils import doc2vecTools
from utils import encoderTools

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


def main():
    '''updateDoctoVecModel('doc2vec', 'doc2vecUpdated')
    # test the model
    testdoc2vecModel('doc2vec', lee_test_file)
    exit()'''
    # create the encoder model
    encoderTools.createEncoderModel(lee_train_file)

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

                                network.fileTransfer('encoder', connection)

                                print(sys.stderr, 'Sending complete. Closing connection to:', client_address)
                                break
                            elif "doc2vec" in str(data):
                                print(sys.stderr, 'Connection from client:', client_address)
                                print(sys.stderr, 'sending doc2vec model to the client')

                                network.fileTransfer('doc2vec', connection)

                                print(sys.stderr, 'Sending complete. Closing connection to:', client_address)
                                break
                        if "Sending" in str(data):
                            print(sys.stderr, 'Connection from client:', client_address)
                            print(sys.stderr, 'receiving doc2vec model from the client')

                            # receive the file
                            network.fileReception(connection)

                            print(sys.stderr, 'Reception complete. Closing connection to:', client_address)

                            # TODO: Update the doc2vec model
                            doc2vecTools.updateDoctoVecModelServer('doc2vec', 'doc2vecUpdated')
                            # test the model
                            doc2vecTools.testdoc2vecModel('doc2vecUpdated', lee_test_file)

                            # update the encoder model with the Updated doc2vec model
                            encoderTools.updateEncoderModel('doc2vecUpdated')
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

