#!/usr/bin/env python3.6

# Kunal Mukherjee
# 4/21/20
# Federated Learning for Image Classification
# imageMain.py
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

MnistVariables = collections.namedtuple(
        'MnistVariables', 'weights bias num_examples loss_sum accuracy_sum')

# creates the variables
def create_mnist_variables():
  return MnistVariables(
      weights=tf.Variable(
          lambda: tf.zeros(dtype=tf.float32, shape=(784, 10)),
          name='weights',
          trainable=True),
      bias=tf.Variable(
          lambda: tf.zeros(dtype=tf.float32, shape=(10)),
          name='bias',
          trainable=True),
      num_examples=tf.Variable(0.0, name='num_examples', trainable=False),
      loss_sum=tf.Variable(0.0, name='loss_sum', trainable=False),
      accuracy_sum=tf.Variable(0.0, name='accuracy_sum', trainable=False))


# define the forward pass method that computes loss,
# emits predictions, and updates the cumulative statistics
# for a single batch of input data
def mnist_forward_pass(variables, batch):
  y = tf.nn.softmax(tf.matmul(batch['x'], variables.weights) + variables.bias)
  predictions = tf.cast(tf.argmax(y, 1), tf.int32)

  flat_labels = tf.reshape(batch['y'], [-1])
  loss = -tf.reduce_mean(
      tf.reduce_sum(tf.one_hot(flat_labels, 10) * tf.math.log(y), axis=[1]))
  accuracy = tf.reduce_mean(
      tf.cast(tf.equal(predictions, flat_labels), tf.float32))

  num_examples = tf.cast(tf.size(batch['y']), tf.float32)

  variables.num_examples.assign_add(num_examples)
  variables.loss_sum.assign_add(loss * num_examples)
  variables.accuracy_sum.assign_add(accuracy * num_examples)

  return loss, predictions


# return the average loss and accuracy, as well as the num_examples
def get_local_mnist_metrics(variables):
  return collections.OrderedDict(
      num_examples=variables.num_examples,
      loss=variables.loss_sum / variables.num_examples,
      accuracy=variables.accuracy_sum / variables.num_examples)


# how to aggregate the local metrics emitted
# by each device via get_local_mnist_metrics
@tff.federated_computation
def aggregate_mnist_metrics_across_clients(metrics):
  return collections.OrderedDict(
      num_examples=tff.federated_sum(metrics.num_examples),
      loss=tff.federated_mean(metrics.loss, metrics.num_examples),
      accuracy=tff.federated_mean(metrics.accuracy, metrics.num_examples))


# image class
class MnistModel(tff.learning.Model):

  def __init__(self):
    self._variables = create_mnist_variables()

  @property
  def trainable_variables(self):
    return [self._variables.weights, self._variables.bias]

  @property
  def non_trainable_variables(self):
    return []

  @property
  def local_variables(self):
    return [
        self._variables.num_examples, self._variables.loss_sum,
        self._variables.accuracy_sum
    ]

  @property
  def input_spec(self):
    return collections.OrderedDict(
        x=tf.TensorSpec([None, 784], tf.float32),
        y=tf.TensorSpec([None, 1], tf.int32))

  @tf.function
  def forward_pass(self, batch, training=True):
    del training
    loss, predictions = mnist_forward_pass(self._variables, batch)
    num_examples = tf.shape(batch['x'])[0]
    return tff.learning.BatchOutput(
        loss=loss, predictions=predictions, num_examples=num_examples)

  @tf.function
  def report_local_outputs(self):
    return get_local_mnist_metrics(self._variables)

  @property
  def federated_output_computation(self):
    return aggregate_mnist_metrics_across_clients


def main():
    initializeFunctions()

    testFedTF()

    # interface that allows you to enumerate the set of users
    emnist_train, emnist_test = tff.simulation.datasets.emnist.load_data()

    # get the number of samples
    sample_clients = emnist_train.client_ids[0:NUM_CLIENTS]
    print(sample_clients)

    # get the train data set
    federated_train_data = make_federated_data(emnist_train, sample_clients)

    print('Number of client datasets: {l}'.format(l=len(federated_train_data)))
    print('First dataset: {d}'.format(d=federated_train_data[0]))

    # keras model

    iterative_process = tff.learning.build_federated_averaging_process(
        MnistModel,
        client_optimizer_fn=lambda: tf.keras.optimizers.SGD(learning_rate=0.02))

    state = iterative_process.initialize()
    print('\nstate', state)

    NUM_ROUNDS = 11
    for round_num in range(NUM_ROUNDS):
        state, metrics = iterative_process.next(state, federated_train_data)
        print('round {:2d}, metrics={}'.format(round_num, metrics))

    evaluation = tff.learning.build_federated_evaluation(MnistModel)
    train_metrics = evaluation(state.model, federated_train_data)
    print('\nTrain ', str(train_metrics))

    federated_test_data = make_federated_data(emnist_test, sample_clients)
    test_metrics = evaluation(state.model, federated_test_data)
    print('\nTest ', str(test_metrics))


if __name__ == '__main__':
    main()
