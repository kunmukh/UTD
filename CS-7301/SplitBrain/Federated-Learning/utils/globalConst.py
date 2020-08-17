#!/usr/bin/env python3.6

# Kunal Mukherjee
# 4/3/20
# Federated Learning of Encoders and word2vec

# Global constants for server
# the server listen addr and port
listen_addr = 'localhost'
listen_port = 10000
# server certificate and key
# openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout server.key -out server.crt
server_cert = 'certificates/server.crt'
server_key = 'certificates/server.key'
# client certificate
client_certs = 'certificates/client.crt'


# Global constants for client
# Server information
host_addr = 'localhost'
host_port = 10000
server_sni_hostname = 'fedserver.com'
# client certificate and key
client_cert = 'certificates/client.crt'
client_key = 'certificates/client.key'
# receive 4096 bytes each time
SEPARATOR = "<SEPARATOR>"


# Global const for both
# size of byte
byte_size = 1024
# dict of model files
dictFName = dict({  'encoder': "models/model_seqs2.h5",
                    'doc2vec': "models/doc2vecModel.pickle",
                    'doc2vecUpdated': "models/doc2vecModelUpdated.pickle",
                    'doc2vecUpdatedData': "data/test.csv",
                    'doc2vecUpdatedPosData': "data/test_pos.csv",
                    'doc2vecPosData': "data/train_pos.csv"})
