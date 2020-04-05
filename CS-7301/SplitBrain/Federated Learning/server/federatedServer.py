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

# TODO: remove them and get real dataset
# training and testing dataset
lee_train_file = '../../data/lee_train.txt'
lee_test_file = '../../data/lee_test.txt'


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


def main():
    # create the encoder model
    encoderTools.createEncoderModel(lee_train_file)

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
                            network.fileReception(connection)

                            print(sys.stderr, 'Reception complete. Closing connection to:', client_address)

                            # TODO: Update the doc2vec model
                            doc2vecTools.updateDoctoVecModelServer('doc2vec', 'doc2vecUpdated')
                            # test the model
                            doc2vecTools.testdoc2vecModel('doc2vec', lee_test_file)

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

