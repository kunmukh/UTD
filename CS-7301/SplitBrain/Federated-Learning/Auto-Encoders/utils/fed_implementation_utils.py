#!/usr/bin/env python3.6

# Kunal Mukherjee
# 5/13/20
# Encoder for analogous image detection with Federated Learning helper

# import statements
from keras.datasets import mnist, fashion_mnist
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from PIL import Image
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from random import shuffle
from sklearn.model_selection import train_test_split

import os

# Number of samples to show
SAMPLES = 500

# path where the data is stored
dataPath = os.getcwd() + '/data'

# helper function to get the data
def getData(needMINST, fileNameTrain=None, fileNameTest=None, fileNameAbnormal=None):
    """

    Parameters
    ----------
    needMINST: boolean about do you want MINST dataset or not
    fileNameTrain: file path
    fileNameTest: file path
    fileNameAbnormal: file path

    Returns pandas dataframe x_train, x_test, x_abnormal
    -------

    """
    if needMINST:
        # prepare normal dataset (Mnist)
        (x_train, _), (x_test, _) = mnist.load_data()
        x_train = x_train / 255.  # normalize into [0,1]
        x_test = x_test / 255.

        # prapare abnormal dataset (Fashion Mnist)
        (_, _), (x_abnormal, _) = fashion_mnist.load_data()
        x_abnormal = x_abnormal / 255.

        # # reshape input data according to the model's input tensor
        x_train = x_train.reshape(-1, 28 * 28)
        x_test = x_test.reshape(-1, 28 * 28)
        x_abnormal = x_abnormal.reshape(-1, 28 * 28)
    else:
        x_train_df = pd.read_csv(fileNameTrain)
        x_test_df = pd.read_csv(fileNameTest)
        x_abnormal_df = pd.read_csv(fileNameAbnormal)

        x_train_df = x_train_df.drop(x_train_df.columns[0], axis=1)
        x_test_df = x_test_df.drop(x_test_df.columns[0], axis=1)
        x_abnormal_df = x_abnormal_df.drop(x_abnormal_df.columns[0], axis=1)

        x_train = x_train_df.values
        x_test = x_test_df.values
        x_abnormal = x_abnormal_df.values

        x = np.vstack((x_train, x_test))

        x = MinMaxScaler().fit_transform(x)
        x_abnormal = MinMaxScaler().fit_transform(x_abnormal)

        x_train, x_test = train_test_split(x, test_size=0.25)
        shuffle(x_abnormal)

    return x_train, x_test, x_abnormal


# helper function to print out the feature extracted and
# the original image
def showImage(x, pred_x):
    """
    This function helps display MINST image. Helps with understanding.

    Parameters
    ----------
    x: pandas dataframe of original image
    pred_x: pandas dataframe of feature extracted image

    Returns
    -------

    """
    X1 = np.asarray(x)
    X1 = X1 * 255
    X1 = X1.reshape(28, 28)
    img = Image.fromarray(X1)
    img.show()

    pred1 = np.asarray(pred_x)
    pred1 = pred1 * 255
    pred1 = pred1.reshape(28, 28)
    img = Image.fromarray(pred1)
    img.show()


# helper function to plot the loss
# https://www.linkedin.com/pulse/anomaly-detection-autoencoder-neural-network-applied-urls-daboubi/
def showloss(x_test, x_abnormal, model):
    """

    Parameters
    ----------
    x_test: feature vector for testing
    x_abnormal: feature vector for adnomral
    model: model used to get mse

    Returns: nothing
    -------

    """
    # the entire x set: normal image + abnormal image
    x_concat = np.concatenate([x_test, x_abnormal], axis=0)
    losses = []
    for x in x_concat:
        # compute loss for each test sample
        x = np.expand_dims(x, axis=0)
        loss = model.test_on_batch(x, x)
        losses.append(loss[0])

    # plot
    fig, ax = plt.subplots()

    # plot both the loss
    plt.plot(range(len(losses[:SAMPLES])), losses[:SAMPLES], linestyle='-', linewidth=1, label="normal data", color='blue')
    plt.plot(range(SAMPLES, len(losses)), losses[SAMPLES:], linestyle='-', linewidth=1, label="anomaly data", color='red')

    # create graph
    plt.legend(loc='best')
    plt.grid()
    plt.title("Reconstruction error for different classes")
    plt.ylabel("Reconstruction error")
    plt.xlabel("Data point index")

    # plt.savefig(args.result)
    # plt.clf()


# helper function to plot the mse of X and threshold for the data
def plotLoss(autoencoder, X_test, y_test, threshold, modelName):
    """

    Parameters
    ----------
    autoencoder: the autoencoder model
    X_test: test feature vector
    y_test: label
    threshold: given threshold
    modelName: a string to display

    Returns nothing
    -------

    """
    tn, fp, fn, tp = 0, 0, 0, 0
    error_df = None

    predictions = autoencoder.predict(X_test)
    mse = np.mean(np.power(X_test - predictions, 2), axis=1)

    # showImage(X_test.values[101], predictions[101])
    error_df = pd.DataFrame(list(zip(list(mse.values.reshape(1, SAMPLES + SAMPLES)[0]),
                                    list(y_test.values.reshape(1, SAMPLES + SAMPLES)[0]))),
                                columns=['reconstruction_error', 'true_class'])

    print('\nLoss Test **************************')
    print('threshold', threshold)
    y_pred = [1 if e > threshold else 0 for e in error_df.reconstruction_error.values]
    conf_matrix = confusion_matrix(error_df.true_class, y_pred)

    result = conf_matrix.ravel()
    if len(result) == 4:
        tn, fp, fn, tp = result
    else:
        tp = result

    print('TP:' + str(tp))
    print('FP:' + str(fp))
    print('TN:' + str(tn))
    print('FN:' + str(fn))

    precision = 1. * tp / (tp + fp)
    recall = 1. * tp / (tp + fn)
    f1 = (2 * recall * precision) / (recall + precision)

    accuracy = 1. * (tp + tn) / (tp + tn + fp + fn)

    print('Accuracy:' + str(accuracy))
    print('Precision:' + str(precision))
    print('Recall:' + str(recall))
    print('F1:' + str(f1))

    groups = error_df.groupby('true_class')

    # plot the loss
    fig, ax = plt.subplots()

    for name, group in groups:
        ax.plot(group.index, group.reconstruction_error, marker='o', ms=2, linestyle='',
                label="Abnormal data" if name == 1 else "Normal data", color='red' if name == 1 else 'orange')
    ax.hlines(threshold, ax.get_xlim()[0], ax.get_xlim()[1], colors="green",
              zorder=100, label='Threshold=' + str(np.round(threshold, 3)))
    ax.legend()
    plt.title(modelName + " Reconstruction error for different classes| Accuracy= " + str(accuracy))
    plt.ylabel("Reconstruction error")
    plt.xlabel("Data point index")


# get the mse threshold corresponding to the 80th percentile
# also print out info regarding the threshold
# plot the threshold w.r.t to train data mse
def getThreasholdTrain(autoencoder, X, y_test, modelName):
    """

    Parameters
    ----------
    autoencoder: autoencoder model
    X: dataset
    y_test: label
    modelName: a string that will be used to display

    Returns: the mse threshold that will give 80% accuracy
    -------

    """
    predictions = autoencoder.predict(X)
    mse = np.mean(np.power(X - predictions, 2), axis=1)

    PERCENTILE = 0.8000
    threshold = np.quantile(mse, PERCENTILE)

    # showImage(X_test.values[101], predictions[101])
    error_df = pd.DataFrame(list(zip(list(mse.values.reshape(1, SAMPLES)[0]),
                                     list(y_test.values.reshape(1, SAMPLES)[0]))),
                            columns=['reconstruction_error', 'true_class'])
    y_pred = [1 if e > threshold else 0 for e in error_df.reconstruction_error.values]
    conf_matrix = confusion_matrix(error_df.true_class, y_pred)

    result = conf_matrix.ravel()
    if len(result) == 4:
        tn, fp, fn, tp = result
    else:
        tp = result

    print('\nLoss Train **************************')
    print('TP:' + str(tp))
    print('FP:' + str(fp))
    print('TN:' + str(tn))
    print('FN:' + str(fn))
    accuracy = 1. * (tp + tn) / (tp + tn + fp + fn)

    groups = error_df.groupby('true_class')

    # plot the image
    fig, ax = plt.subplots()

    for name, group in groups:
        ax.plot(group.index, group.reconstruction_error, marker='o', ms=2, linestyle='',
                label="Abnormal data" if name == 1 else "Normal data", color='red' if name == 1 else 'orange')
    ax.hlines(threshold, ax.get_xlim()[0], ax.get_xlim()[1], colors="green",
              zorder=100, label='Threshold=' + str(np.round(threshold, 3)))
    ax.legend()
    plt.title(modelName + " Reconstruction error for different classes| Accuracy= " + str(accuracy))
    plt.ylabel("Reconstruction error")
    plt.xlabel("Data point index")

    return threshold


# get the threshold given a required accuracy and recall
def getThreashold(autoencoder, X_test, y_test, want_accuracy, want_recall):

    """

    Parameters
    ----------
    autoencoder: model used for prediction
    X_test: test feature vector
    y_test: label
    want_accuracy: the required to use to get mse threshold
    want_recall: the required call used to get mse threshold

    Returns the mse threshold
    -------

    """
    predictions = autoencoder.predict(X_test)
    mse = np.mean(np.power(X_test - predictions, 2), axis=1)
    # threshold = np.quantile(mse, 0.9900)

    error_df = pd.DataFrame(list(zip(list(mse.values.reshape(1, SAMPLES + SAMPLES)[0]),
                                     list(y_test.values.reshape(1, SAMPLES + SAMPLES)[0]))),
                            columns=['reconstruction_error', 'true_class'])
    print(error_df)
    fraud_error_df = error_df[error_df['true_class'] == 1]

    # get the threshold
    threshold = 0
    f1 = 0
    recall = 0
    accuracy = 0

    while recall < want_recall or accuracy < want_accuracy:
        print('**************************')
        print('threshold', threshold)
        threshold += .0005
        y_pred = [1 if e > threshold else 0 for e in error_df.reconstruction_error.values]
        conf_matrix = confusion_matrix(error_df.true_class, y_pred)

        result = conf_matrix.ravel()
        if len(result) == 4:
            tn, fp, fn, tp = result
        else:
            tp = result

        precision = 1. * tp / (tp + fp)
        recall = 1. * tp / (tp + fn)
        f1 = (2 * recall * precision) / (recall + precision)
        print('TP:' + str(tp))
        print('FP:' + str(fp))
        print('TN:' + str(tn))
        print('FN:' + str(fn))
        accuracy = 1. * (tp + tn) / (tp + tn + fp + fn)
        print('Accuracy:' + str(accuracy))
        print('Precision:' + str(precision))
        print('Recall:' + str(recall))
        print('F1:' + str(f1))

    groups = error_df.groupby('true_class')

    # plot the loss with the threshold
    fig, ax = plt.subplots()

    for name, group in groups:
        ax.plot(group.index, group.reconstruction_error, marker='o', ms=2, linestyle='',
                label="Abnormal data" if name == 1 else "Normal data", color='red' if name == 1 else 'orange')
    ax.hlines(threshold, ax.get_xlim()[0], ax.get_xlim()[1], colors="green",
              zorder=100, label='Threshold='+str(np.round(threshold,3)))
    ax.legend()
    plt.title("Reconstruction error for different classes| Accuracy= " + str(accuracy))
    plt.ylabel("Reconstruction error")
    plt.xlabel("Data point index")

    return threshold


# the driver function
def driver(model, modelName, MINSTData):
    """
    driver function

    Parameters
    ----------
    model: model that will used to get the threshold and do evaluation
    modelName: a string to display in the plot
    MINSTData: a boolean to say if we want to use MINST data or not

    Returns nothing
    -------

    """

    if MINSTData:
        X_train, x_test, x_abnormal = getData(True)
    else:
        X_train, x_test, x_abnormal = getData(False,
                                                dataPath+"/benignK.csv",
                                                dataPath+"/benignTestK.csv",
                                                dataPath+"/anaK.csv")

    # get the 80th percentile of the train threshold
    # get the threshold that will give 80% training accuracy
    threshold = getThreasholdTrain(model,
                                   pd.DataFrame(X_train[:SAMPLES]),
                                   pd.DataFrame([0 for _ in range(SAMPLES)]),
                                   modelName)

    '''# plot the loss for given samples
    showloss(x_test[:SAMPLES], x_abnormal[:SAMPLES], model)

    # generate the test sample( 500 good image + 500 abnormal image)
    X_test = pd.DataFrame(np.concatenate([x_test[:SAMPLES], x_abnormal[0:SAMPLES]], axis=0))
    Y_test = pd.DataFrame([0 for _ in range(SAMPLES)] + [1 for _ in range(SAMPLES)])

    # uncomment to shuffle the data
    shuffleFlag = False
    if shuffleFlag:
        # shuffle the data
        data = np.hstack((X_test.values, Y_test.values))
        np.random.shuffle(data)
        data = pd.DataFrame(data)
        X_test = data.iloc[:, :-1]
        Y_test = data.iloc[:, -1]

    # plot the mse loss of (combined: test + abnormal) X and threshold for the test data
    plotLoss(model, X_test, Y_test, threshold, modelName)'''

    # generate the test sample( 2 * 500 test image)
    X_test = pd.DataFrame(np.concatenate([x_test[:SAMPLES], x_test[SAMPLES:2*SAMPLES]], axis=0))
    Y_test = pd.DataFrame([0 for _ in range(SAMPLES)] + [0 for _ in range(SAMPLES)])

    # plot the mse loss of X test using the given mse threshold
    plotLoss(model, X_test, Y_test, threshold, modelName)

    # generate the abnormal sample( 2*  500 abnormal image)
    X_test = pd.DataFrame(np.concatenate([x_abnormal[:SAMPLES], x_abnormal[SAMPLES:2 * SAMPLES]], axis=0))
    Y_test = pd.DataFrame([1 for _ in range(SAMPLES)] + [1 for _ in range(SAMPLES)])

    # plot the mse loss of X abnormal using the given mse threshold
    plotLoss(model, X_test, Y_test, threshold, modelName)

    print('\n\nThreshold', threshold)

    # uncomment if you want to get threshold for a given
    # accuracy and recall
    '''# define the accuracy and recall
    want_accuracy, want_recall = 0.90, 0.5
    getThreashold(model, X_test, Y_test, want_accuracy, want_recall)'''

    plt.show()