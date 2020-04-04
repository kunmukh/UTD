#!/usr/bin/env python3.6

# Kunal Mukherjee
# 3/15/20
# Federated Learning of Encoders and word2vec
# federatedClient.py

# import statements
import socket
import sys
import ssl


# utilities
from utils import dateFormat
from utils import network
from utils import doc2vecTools

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
lee_train_file = '../../data/lee_train.txt'
lee_test_file = '../../data/lee_test.txt'


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
            network.fileReception(connection)

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
        network.fileTransfer('doc2vecUpdated', connection)

    finally:
        print(sys.stderr, 'closing socket')
        sock.close()
# --------------------------------------------------


def main():
    # get the initial encoder and doc2vec model
    getInitialModels()

    # do the prediction from the model data
    doc2vecTools.testdoc2vecModel('doc2vec', lee_test_file)

    # TODO: create the updated doc2vec model
    # the new training file
    doc2vecTools.updateDoctoVecModelClient(doc2vecTools.dataProcessing(lee_test_file, 'train'),
                                           dictModelFName['doc2vec'])


    # send the updated doc2vec model
    senddoc2vecUpdatedModel()


if __name__ == '__main__':
    main()