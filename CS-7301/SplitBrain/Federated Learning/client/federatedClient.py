#!/usr/bin/env python3.6

# Kunal Mukherjee
# 3/15/20
# Federated Learning of Encoders and word2vec
# federatedClient.py

# import statements
import socket
import sys
import ssl


# Global constants
# Server information
host_addr = 'localhost'
host_port = 10000
server_sni_hostname = 'fedserver.com'
# server certificate
server_cert = 'server.crt'
# client certificate and key
client_cert = 'client.crt'
client_key = 'client.key'


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

def main():
    # create the connection the the server
    sock, connection = initializeConnection(host_addr, host_port)

    try:
        # Send data
        message = 'INITIALThis is the message. It will be repeated.'
        print(sys.stderr, 'sending "%s"' % message)
        connection.sendall(message.encode('UTF-8'))

        # Look for the response
        amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = connection.recv(128)
            amount_received += len(data)
            print(sys.stderr, 'received "%s"' % data)
            if "END" in str(data):
                break

    finally:
        print(sys.stderr, 'closing socket')
        sock.close()


if __name__ == '__main__':
    main()