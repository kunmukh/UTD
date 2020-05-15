#!/usr/bin/env python3.6

# Kunal Mukherjee
# 5/13/20
# Encoder for analogous image detection with Federated Learning

# import statement
import numpy as np
import pandas as pd
import random
import cv2
import os
from imutils import paths

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Dense
from tensorflow.keras import backend as K

from keras.models import load_model
from utils import fed_implementation_utils as fu
from sklearn.metrics import confusion_matrix

# global variable
img_path = '../../data/MINSTtrainingSet'


# load the image path
def load(paths, verbose=-1):
    '''expects images for each class in seperate dir,
    e.g all digits in 0 class in the directory named 0 '''
    data = list()
    labels = list()
    # loop over the input images
    for (i, imgpath) in enumerate(paths):
        # load the image and extract the class labels
        im_gray = cv2.imread(imgpath, cv2.IMREAD_GRAYSCALE)
        image = np.array(im_gray).flatten()
        label = imgpath.split(os.path.sep)[-2]
        # scale the image to [0, 1] and add to list
        data.append(image/255)
        labels.append(label)
        # show an update every `verbose` images
        if verbose > 0 and i > 0 and (i + 1) % verbose == 0:
            print("[INFO] processed {}/{}".format(i + 1, len(paths)))
    # return a tuple of the data and labels
    return data, labels


# create client dataset
def create_clients(image_list, num_clients=10, initial='clients'):
    ''' return: a dictionary with keys clients' names and value as
                data shards - tuple of images and label lists.
        args:
            image_list: a list of numpy arrays of training images
            label_list:a list of binarized labels for each image
            num_client: number of fedrated members (clients)
            initials: the clients'name prefix, e.g, clients_1

    '''

    # create a list of client names
    client_names = ['{}_{}'.format(initial, i + 1) for i in range(num_clients)]

    # randomize the data
    data = image_list
    random.shuffle(data)

    # shard data and place at each client
    size = len(data) // num_clients
    shards = [data[i:i + size] for i in range(0, size * num_clients, size)]

    # number of clients must equal number of shards
    assert (len(shards) == len(client_names))

    return {client_names[i]: shards[i] for i in range(len(client_names))}


# process each of the client’s data into tensorflow data set and batch them
def batch_data(data_shard, bs=32):
    '''Takes in a clients data shard and create a tfds object off it
    args:
        shard: a data constituting a client's data shard
        bs:batch size
    return:
        tfds object'''

    # seperate shard into data and labels lists
    dataset = tf.data.Dataset.from_tensor_slices((list(data_shard), list(data_shard)))

    return dataset.shuffle(len(list(data_shard))).batch(bs)


# simple 3 layer perceptron
class SimpleMLP:
    @staticmethod
    def build(shape, classes):

        hidden_dim = int(shape / 2)

        model = Sequential()
        model.add(Dense(hidden_dim, input_shape=(shape,)))
        model.add(Activation("tanh"))
        model.add(Dense(hidden_dim))
        model.add(Activation("relu"))
        model.add(Dense(hidden_dim))
        model.add(Activation("relu"))
        model.add(Dense(classes))
        model.add(Activation("tanh"))
        return model


# calculates the proportion of a client’s local training data with
# the overall training data held by all clients.
def weight_scalling_factor(clients_trn_data, client_name):
    client_names = list(clients_trn_data.keys())
    # get the bs - batch size
    bs = list(clients_trn_data[client_name])[0][0].shape[0]
    # first calculate the total training data points across clients
    global_count = sum(
        [tf.data.experimental.cardinality(clients_trn_data[client_name]).numpy() for client_name in client_names]) * bs
    # get the total number of data points held by a client
    local_count = tf.data.experimental.cardinality(clients_trn_data[client_name]).numpy() * bs
    return local_count / global_count


# scales each of the local model’s weights based the value of their
# scaling factor calculated in weight_scalling_factor
def scale_model_weights(weight, scalar):
    '''function for scaling a models weights'''
    weight_final = []
    steps = len(weight)
    for i in range(steps):
        weight_final.append(scalar * weight[i])
    return weight_final


# sums all clients’ scaled weights together
def sum_scaled_weights(scaled_weight_list):
    '''Return the sum of the listed scaled weights. The is equivalent to scaled avg of the weights'''
    avg_grad = list()
    # get the average grad across all client gradients
    for grad_list_tuple in zip(*scaled_weight_list):
        layer_mean = tf.math.reduce_sum(grad_list_tuple, axis=0)
        avg_grad.append(layer_mean)

    return avg_grad


def main():

    # get the path list using the path object
    image_paths = list(paths.list_images(img_path))

    # apply our function
    image_list, label_list = load(image_paths, verbose=10000)

    # print(pd.DataFrame(label_list[0:10]))

    # create clients
    clients = create_clients(image_list, num_clients=10, initial='client')

    x_test = image_list[0:len(image_list):400]

    # process and batch the training data for each client
    clients_batched = dict()
    for (client_name, data) in clients.items():
        clients_batched[client_name] = batch_data(data)

    # local constants
    # the number global epochs (aggregations)
    comms_round = 10

    # create optimizer constants
    loss = 'mean_squared_error'
    metrics = ['accuracy']
    optimizer = 'adam'

    # FEDERATED MODEL TRAINING
    # initialize global model
    smlp_global = SimpleMLP()
    global_model = smlp_global.build(len(image_list[0]), len(image_list[0]))

    # commence global training loop
    for comm_round in range(comms_round):

        # get the global model's weights - will serve as the initial weights for all local models
        global_weights = global_model.get_weights()

        # initial list to collect local model weights after scalling
        scaled_local_weight_list = list()

        # randomize client data - using keys
        client_names = list(clients_batched.keys())
        random.shuffle(client_names)

        # loop through each client and create new local model
        for client in client_names:
            smlp_local = SimpleMLP()
            local_model = smlp_local.build(len(image_list[0]), len(image_list[0]))
            local_model.compile(loss=loss,
                                optimizer=optimizer,
                                metrics=metrics)

            # set local model weight to the weight of the global model
            local_model.set_weights(global_weights)

            # fit local model with client's data #  validation_data=(x_test, x_test),np.asarray(X)
            x_val = tf.data.Dataset.from_tensor_slices((list(x_test), list(x_test))).batch(len(list(x_test)))
            print('Current Training', client)
            local_model.fit(clients_batched[client], validation_data=x_val, epochs=5, verbose=1)

            # scale the model weights and add to list
            scaling_factor = weight_scalling_factor(clients_batched, client)
            scaled_weights = scale_model_weights(local_model.get_weights(), scaling_factor)
            scaled_local_weight_list.append(scaled_weights)

            # clear session to free memory after each communication round
            K.clear_session()

        # to get the average over all the local model, we simply take the sum of the scaled weights
        average_weights = sum_scaled_weights(scaled_local_weight_list)

        # update global model
        global_model.set_weights(average_weights)

        print(comm_round, "Done")

    # save the auto encoder
    global_model.save("model.h5")

    fu.driver(global_model, 'Federated')


if __name__ == '__main__':
    main()