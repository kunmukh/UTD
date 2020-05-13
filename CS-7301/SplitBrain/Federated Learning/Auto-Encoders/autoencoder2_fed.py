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
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD
from tensorflow.keras import backend as K

from utils import fed_implementation_utils

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
def create_clients(image_list, label_list, num_clients=10, initial='clients'):
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
    data = list(zip(image_list, label_list))
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
        shard: a data, label constituting a client's data shard
        bs:batch size
    return:
        tfds object'''

    # seperate shard into data and labels lists
    data, label = zip(*data_shard)
    dataset = tf.data.Dataset.from_tensor_slices((list(data), list(label)))

    return dataset.shuffle(len(label)).batch(bs)


# simple 3 layer perceptron
class SimpleMLP:
    @staticmethod
    def build(shape, classes):
        model = Sequential()
        model.add(Dense(200, input_shape=(shape,)))
        model.add(Activation("relu"))
        model.add(Dense(200))
        model.add(Activation("relu"))
        model.add(Dense(classes))
        model.add(Activation("softmax"))
        return model


def main():

    # get the path list using the path object
    image_paths = list(paths.list_images(img_path))

    # apply our function
    image_list, label_list = load(image_paths, verbose=10000)
    # print(pd.DataFrame(label_list[0:10]))

    # binarize the labels
    lb = LabelBinarizer()
    label_list = lb.fit_transform(label_list)
    # print(pd.DataFrame(label_list[0:10]))

    # split data into training and test set
    X_train, X_test, y_train, y_test = train_test_split(image_list,
                                                        label_list,
                                                        test_size=0.1,
                                                        random_state=42)

    # create clients
    clients = create_clients(X_train, y_train, num_clients=10, initial='client')

    # process and batch the training data for each client
    clients_batched = dict()
    for (client_name, data) in clients.items():
        clients_batched[client_name] = batch_data(data)

    # process and batch the test set
    test_batched = tf.data.Dataset.from_tensor_slices((X_test, y_test)).batch(len(y_test))

    # local constants
    comms_round = 100

    # create optimizer constants
    lr = 0.01
    loss = 'categorical_crossentropy'
    metrics = ['accuracy']
    optimizer = SGD(lr=lr,
                    decay=lr / comms_round,
                    momentum=0.9
                    )



if __name__ == '__main__':
    main()