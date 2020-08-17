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
from utils import globalConst

# number of models
models = ['encoder', 'doc2vec']


# initialize the connection with the server
# return the connection socket
def initializeConnection(server_ip, server_port):
    # Load the ssl context
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=globalConst.server_cert)
    context.load_cert_chain(certfile=globalConst.client_cert, keyfile=globalConst.client_key)

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # ssl context wrap
    connection = context.wrap_socket(sock, server_side=False, server_hostname=globalConst.server_sni_hostname)

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


# get the initial encoder and doc2vec model
def getInitialModels():
    # get the initial models: encoder and doc2vec
    for model in models:
        # create the connection the the server
        sock, connection = initializeConnection(globalConst.host_addr, globalConst.host_port)

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


'''# send the updated doc2vec model
def senddoc2vecUpdatedModel():
    # send the updated doc2vec model
    # create the connection the the server
    sock, connection = initializeConnection(globalConst.host_addr, globalConst.host_port)

    try:
        # Send the request to get encoder and doc2vec model
        message = 'Connection Sending doc2vec model'
        print(sys.stderr, 'sending "%s"' % message)
        connection.sendall(message.encode('UTF-8'))

        # receive the file
        network.fileTransfer('doc2vecUpdated', connection)

    finally:
        print(sys.stderr, 'closing socket')
        sock.close()'''


# send the updated doc2vec model
def senddoc2vecUpdatedModelData():
    # send the updated doc2vec model
    # create the connection the the server
    sock, connection = initializeConnection(globalConst.host_addr, globalConst.host_port)

    try:
        # Send the request to get encoder and doc2vec model
        message = 'Connection Sending doc2vec model data'
        print(sys.stderr, 'sending "%s"' % message)
        connection.sendall(message.encode('UTF-8'))

        # receive the file
        network.fileTransfer('doc2vecUpdatedData', connection)

    finally:
        print(sys.stderr, 'closing socket')
        sock.close()


def main():
    # get the initial encoder and doc2vec model
    getInitialModels()

    # do the prediction from the model data
    doc2vecTools.testdoc2vecModel('doc2vec', globalConst.dictFName['doc2vecUpdatedData'])

    # TODO: create the updated doc2vec model
    '''# the new training file
    doc2vecTools.updateDoctoVecModelClient(
        doc2vecTools.dataProcessing(globalConst.dictFName['doc2vecUpdatedData'], 'train'),
        globalConst.dictFName['doc2vec'])'''

    doc2vecTools.updateDoctoVecModelClient(
        doc2vecTools.dataProcessingCSV(globalConst.dictFName['doc2vecUpdatedPosData']),
        globalConst.dictFName['doc2vec'])

    '''# send the updated doc2vec model
    senddoc2vecUpdatedModel()'''

    # send the new doc2vec model data
    senddoc2vecUpdatedModelData()


if __name__ == '__main__':
    main()