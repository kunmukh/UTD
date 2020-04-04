#!/usr/bin/env python3.6

# Kunal Mukherjee
# 4/3/20
# Federated Learning of Encoders and word2vec

import os
import tqdm

# dict of model files
dictModelFName = dict({'encoder': "models/model_seqs2.h5",
                       'doc2vec': "models/doc2vecModel.pickle",
                       'doc2vecUpdated': "models/doc2vecModelUpdated.pickle"})

# size of byte
byte_size = 1024


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