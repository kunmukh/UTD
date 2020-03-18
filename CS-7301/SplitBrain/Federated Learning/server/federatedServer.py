#!/usr/bin/env python3.6

# Kunal Mukherjee
# 3/15/20
# Federated Learning of Encoders and word2vec
# federatedServer.py

# import statements
import socket
import sys
import ssl
import os

# Global constants
# the server listen addr and port
listen_addr = 'localhost'
listen_port = 10000
# server certificate and key
server_cert = 'server.crt'
server_key = 'server.key'
# client certificate
client_certs = 'client.crt'


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
                    data = connection.recv(128)
                    print(sys.stderr, 'received "%s"' % data)

                    if data:

                        if "INITIAL" in str(data):
                            print(sys.stderr, 'First Transmission', client_address)
                            print(sys.stderr, 'sending data back to the client')
                            connection.sendall(str(data).replace('INITIAL', 'END').encode('UTF-8'))
                        else:
                            print(sys.stderr, 'sending data back to the client')
                            connection.sendall(data)

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

