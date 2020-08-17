#!/usr/bin/env python3.6

# Kunal Mukherjee
# 4/24/20
# Encoder for analogous image detection

# check version of modules
# python3 --version
# output: Python 3.6.6
# python3 -c 'import tensorflow as tf; print(tf.__version__)'
# output: 2.0.0
# python3 -c 'import keras; print(keras.__version__)'
# output: 2.3.1

# import statements
from keras.layers import Input, Dense
import numpy as np
from keras import regularizers
from keras.models import Model, load_model
import pandas as pd

from utils import fed_implementation_utils as fu

import psutil
import os

# path where the data is stored
dataPath = os.getcwd() + '/data'

# training of the autoencoder model
# https://github.com/otenim/AnomalyDetectionUsingAutoencoder
def getAutoencoderModel(X_train, x_test):
    """
    This function used the training and test data to create an autoencoder model.

    :param X_train: feature vector for training the model
    :param x_test: feature vector for testing the model
    :return: returns the autoencoder model
    """
    # number of features
    input_dim = X_train.shape[1]
    # bottle necking the feature
    encoding_dim = int(input_dim/ 2)
    hidden_dim = int(encoding_dim / 2)
    input_layer = Input(shape=(input_dim,))

    # NN shape
    encoder = Dense(encoding_dim, activation="tanh",
                    activity_regularizer=regularizers.l1(10e-5))(input_layer)
    encoder = Dense(hidden_dim, activation="relu")(encoder)
    decoder = Dense(encoding_dim, activation='relu')(encoder)
    decoder = Dense(input_dim, activation='tanh')(decoder)

    autoencoder = Model(inputs=input_layer, outputs=decoder)

    # number of epochs and batch size
    nb_epoch = 30
    batch_size = 128

    autoencoder.compile(optimizer='adam',
                        loss='mean_squared_error',
                        metrics=['accuracy'])

    autoencoder.fit(X_train, X_train, epochs=nb_epoch, batch_size=batch_size, shuffle=True,
                              validation_data=(x_test, x_test), verbose=1)

    # save the auto encoder
    autoencoder.save("model.h5")
    # load the auto encoder
    autoencoder = load_model('model.h5')
    return autoencoder


# the driver function
def main():
    """
    takes the data, creates the model and sends the model evaluation

    Returns nothing
    -------

    """
    print('PID: ', os.getpid())
    print('Press ANY KEY to continue >>>>')
    input()
    
    X_train, x_test, _ = fu.getData(False,
        dataPath+"/benignK.csv", 
        dataPath+"/benignTestK.csv", 
        dataPath+"/anaK.csv") # anomalous

    # build the auto-encoder model
    model = getAutoencoderModel(X_train, x_test)

    # uncomment if you already have a trained model
    # model = load_model('model.h5')

    fu.driver(model, 'Non-Federated', False)


if __name__ == '__main__':
    """
    main driver program 
    """
    main()