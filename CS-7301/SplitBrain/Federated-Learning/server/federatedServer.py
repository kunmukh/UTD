#!/usr/bin/env python3.6

# Kunal Mukherjee
# 3/15/20
# Federated Learning of Encoders and word2vec
# federatedServer.py

# import statements
import socket
import sys
import ssl

# utilities
from utils import dateFormat
from utils import network
from utils import doc2vecTools
from utils import encoderTools
from utils import globalConst


# initialize a socket with ip and port
# return a ssl context and the socket
def initializeSocket(ip_addr, port):

    # create the ssl context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_cert_chain(certfile=globalConst.server_cert, keyfile=globalConst.server_key)
    context.load_verify_locations(cafile=globalConst.client_certs)

    # create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = (ip_addr, port)
    print(sys.stderr, 'starting up on %s port %s' % server_address)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    return sock, context


# TODO remove
def dataMani():
    import pandas as pd
    from tensorflow import keras
    import numpy as np

    # save np.load
    np_load_old = np.load

    # modify the default parameters of np.load
    np.load = lambda *a, **k: np_load_old(*a, allow_pickle=True, **k)

    data = keras.datasets.imdb
    # separate the data into training and testing data set
    (train_data, train_labels), (test_data, test_labels) = data.load_data(num_words=88000)
    # restore np.load for future normal usage
    np.load = np_load_old

    print(train_data[0])
    print(train_labels[0])

    index = data.get_word_index()
    reverse_index = dict([(value, key) for (key, value) in index.items()])
    decoded = " ".join([reverse_index.get(i - 3, "#") for i in train_data[0]])
    print(decoded)

    data = []
    data_label = []

    for count, d in enumerate(train_data):
        data.append(" ".join([reverse_index.get(i - 3, "#") for i in d]))
        data_label.append(train_labels[count])

    my_dict = {'Rating': data_label,
               'Plot': data}

    df = pd.DataFrame(my_dict)

    print(df)

    df.to_csv('data/train.csv')

    pos_df = df.loc[df['Rating'] == 1]
    neg_df = df.loc[df['Rating'] == 0]

    print(pos_df)
    print(neg_df)

    pos_df.to_csv('data/train_pos.csv')
    neg_df.to_csv('data/train_neg.csv')

    data = []
    data_label = []

    for count, d in enumerate(test_data):
        data.append(" ".join([reverse_index.get(i - 3, "#") for i in d]))
        data_label.append(test_labels[count])

    my_dict = {'Rating': data_label,
               'Plot': data}

    df2 = pd.DataFrame(my_dict)

    print(df2)

    df2.to_csv('data/test.csv')

    pos_df2 = df2.loc[df['Rating'] == 1]
    neg_df2 = df2.loc[df['Rating'] == 0]

    print(pos_df2)
    print(neg_df2)

    pos_df2.to_csv('data/test_pos.csv')
    neg_df2.to_csv('data/test_neg.csv')

    exit()


def main():
    # create the encoder model
    encoderTools.createEncoderModel(globalConst.dictFName['doc2vecPosData'])

    # initialize a socket with ip and port
    sock, sslContext = initializeSocket(globalConst.listen_addr, globalConst.listen_port)

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
                    data = connection.recv(globalConst.byte_size)
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
                            network.fileReception(connection, True)

                            print(sys.stderr, 'Reception complete. Closing connection to:', client_address)

                            # TODO: Update the doc2vec model
                            # doc2vecTools.updateDoctoVecModelServer('doc2vec', 'doc2vecUpdated')

                            '''doc2vecTools.updateDoctoVecModelServer(globalConst.dictFName['doc2vec'],
                                                                   doc2vecTools.dataProcessing(
                                                                       globalConst.dictFName['doc2vecUpdatedData'],
                                                                       'train'))'''
                            doc2vecTools.updateDoctoVecModelServer(
                                doc2vecTools.dataProcessingCSV(globalConst.dictFName['doc2vecUpdatedData']),
                                globalConst.dictFName['doc2vec'])

                            # test the model
                            '''doc2vecTools.testdoc2vecModel('doc2vecUpdated',
                                                          globalConst.dictFName['doc2vecUpdatedData'])'''
                            doc2vecTools.testdoc2vecModel('doc2vecUpdated',
                                                          globalConst.dictFName['doc2vecUpdatedData'])

                            # update the encoder model with the Updated doc2vec model
                            encoderTools.updateEncoderModel('doc2vecUpdated',
                                                            globalConst.dictFName['doc2vecPosData'])
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

