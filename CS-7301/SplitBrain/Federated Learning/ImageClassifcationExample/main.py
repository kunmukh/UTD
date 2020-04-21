#!/usr/bin/env python3.6

# Kunal Mukherjee
# 4/21/20
# Federated Learning for Image Classification
# main.py
# Tutorial: https://www.tensorflow.org/federated/tutorials/federated_learning_for_image_classification

import collections

import numpy as np
import tensorflow as tf
import tensorflow_federated as tff
from matplotlib import pyplot as plt


def initializeFunctions():
    # It switches all global behaviors that are different
    # between TensorFlow 1.x and 2.x to behave as intended for 2.x.
    tf.compat.v1.enable_v2_behavior()
    np.random.seed(0)


def testFedTF():
    # test to see federated computing is working
    print(tff.federated_computation(lambda: 'Hello, World!')())


def batch_format_fn(element):
    """Flatten a batch `pixels` and return the features as an `OrderedDict`."""
    return collections.OrderedDict(
        x=tf.reshape(element['pixels'], [-1, 784]),
        y=tf.reshape(element['label'], [-1, 1]))


NUM_CLIENTS = 10
NUM_EPOCHS = 5
BATCH_SIZE = 20
SHUFFLE_BUFFER = 100
PREFETCH_BUFFER=10


# flatten the 28x28 images into 784-element arrays,
# shuffle the individual examples, organize them into batches,
# and renames the features from pixels and
# label to x and y for use with Keras
def preprocess(dataset):

  return dataset.repeat(NUM_EPOCHS).shuffle(SHUFFLE_BUFFER).batch(
      BATCH_SIZE).map(batch_format_fn).prefetch(PREFETCH_BUFFER)


# will construct a list of datasets
# from the given set of users
# as an input to a round of training or evaluation
def make_federated_data(client_data, client_ids):
  return [
      preprocess(client_data.create_tf_dataset_for_client(x))
      for x in client_ids
  ]


# create a keras model
def create_keras_model():
  return tf.keras.models.Sequential([
      tf.keras.layers.Input(shape=(784,)),
      tf.keras.layers.Dense(10, kernel_initializer='zeros'),
      tf.keras.layers.Softmax(),
  ])

preprocessed_example_dataset = None

# passing the model and a sample data batch as arguments
def model_fn():
    global preprocessed_example_dataset
    # We _must_ create a new model here, and _not_ capture it from an external
    # scope. TFF will call this within different graph contexts.
    keras_model = create_keras_model()
    return tff.learning.from_keras_model(
        keras_model,
        input_spec=preprocessed_example_dataset.element_spec,
        loss=tf.keras.losses.SparseCategoricalCrossentropy(),
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy()])


def main():
    global preprocessed_example_dataset

    initializeFunctions()

    testFedTF()

    # interface that allows you to enumerate the set of users
    emnist_train, emnist_test = tff.simulation.datasets.emnist.load_data()

    # look at the client id
    example_dataset = emnist_train.create_tf_dataset_for_client(
        emnist_train.client_ids[0])

    # pre-process the dataset
    preprocessed_example_dataset = preprocess(example_dataset)

    # get the number of samples
    sample_clients = emnist_train.client_ids[0:NUM_CLIENTS]
    # get the train data set
    federated_train_data = make_federated_data(emnist_train, sample_clients)

    iterative_process = tff.learning.build_federated_averaging_process(
        model_fn,
        client_optimizer_fn=lambda: tf.keras.optimizers.SGD(learning_rate=0.02),
        server_optimizer_fn=lambda: tf.keras.optimizers.SGD(learning_rate=1.0))

    # print('\nsignature', str(iterative_process.initialize.type_signature))

    state = iterative_process.initialize()
    print('\nstate', state)

    NUM_ROUNDS = 11
    for round_num in range(NUM_ROUNDS):
        state, metrics = iterative_process.next(state, federated_train_data)
        print('round {:2d}, metrics={}'.format(round_num, metrics))

    evaluation = tff.learning.build_federated_evaluation(model_fn)
    train_metrics = evaluation(state.model, federated_train_data)
    print('\nTrain ', str(train_metrics))

    federated_test_data = make_federated_data(emnist_test, sample_clients)
    test_metrics = evaluation(state.model, federated_test_data)
    print('\nTest ', str(test_metrics))



def mainTemp():
    global preprocessed_example_dataset
    initializeFunctions()

    testFedTF()

    # interface that allows you to enumerate the set of users
    emnist_train, emnist_test = tff.simulation.datasets.emnist.load_data()
    print(len(emnist_train.client_ids))
    # look at the element structure
    print(emnist_train.element_type_structure)

    # look at the client id
    example_dataset = emnist_train.create_tf_dataset_for_client(
        emnist_train.client_ids[0])

    # return the next item in the iterator
    example_element = next(iter(example_dataset))

    # look at the label
    print(example_element['label'].numpy())

    '''# show the data set
    plt.imshow(example_element['pixels'].numpy(), cmap='gray', aspect='equal')
    plt.grid(False)
    _ = plt.show()'''

    # pre-process the dataset
    preprocessed_example_dataset = preprocess(example_dataset)

    sample_batch = tf.nest.map_structure(lambda x: x.numpy(),
                                         next(iter(preprocessed_example_dataset)))
    # print the sample batch
    print(sample_batch)

    # get the number of samples
    sample_clients = emnist_train.client_ids[0:NUM_CLIENTS]
    # get the train data set
    federated_train_data = make_federated_data(emnist_train, sample_clients)

    print('Number of client datasets: {l}'.format(l=len(federated_train_data)))
    print('First dataset: {d}'.format(d=federated_train_data[0]))

    # model_fn()

    iterative_process = tff.learning.build_federated_averaging_process(
        model_fn,
        client_optimizer_fn=lambda: tf.keras.optimizers.SGD(learning_rate=0.02),
        server_optimizer_fn=lambda: tf.keras.optimizers.SGD(learning_rate=1.0))

    print('\nsignature', str(iterative_process.initialize.type_signature))

    state = iterative_process.initialize()
    print('\nstate', state)

    state, metrics = iterative_process.next(state, federated_train_data)
    print('\nround  1, metrics={}'.format(metrics))

    print('\n\n')
    NUM_ROUNDS = 11
    for round_num in range(2, NUM_ROUNDS):
        state, metrics = iterative_process.next(state, federated_train_data)
        print('round {:2d}, metrics={}'.format(round_num, metrics))\


    '''# summary writer directory
    logdir = "/tmp/logs/scalars/training/"
    summary_writer = tf.summary.create_file_writer(logdir)
    state = iterative_process.initialize()

    # Plot the relevant scalar metrics with the same summary writer.
    with summary_writer.as_default():
        for round_num in range(1, NUM_ROUNDS):
            state, metrics = iterative_process.next(state, federated_train_data)
            for name, value in metrics._asdict().items():
                tf.summary.scalar(name, value, step=round_num)
    # terminal "tensorboard --logdir /tmp/logs/scalars/ --port=0"'''



if __name__ == '__main__':
    main()