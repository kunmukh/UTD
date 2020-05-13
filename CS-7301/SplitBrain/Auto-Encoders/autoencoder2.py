# Kunal Mukherjee
# 4/24/20
# Encoder for analogous image detection

from keras.datasets import mnist, fashion_mnist
from keras.layers import Input, Dense
import numpy as np
from keras import regularizers
from keras.models import Model, load_model
import matplotlib.pyplot as plt
from sklearn.metrics import (confusion_matrix, precision_recall_curve, auc,
                             roc_curve, recall_score, classification_report, f1_score,
                             precision_recall_fscore_support)
from PIL import Image
import pandas as pd

SAMPLES = 100

def getData():
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

    return x_train, x_test, x_abnormal


# https://github.com/otenim/AnomalyDetectionUsingAutoencoder
def getAutoencoderModel(X_train, x_test):
    # number of features
    input_dim = X_train.shape[1]
    hidden_dim = int(input_dim / 2)

    input_layer = Input(shape=(input_dim,))

    encoder = Dense(input_dim, activation="tanh",
                    activity_regularizer=regularizers.l1(10e-5))(input_layer)
    encoder = Dense(hidden_dim, activation="relu")(encoder)
    decoder = Dense(input_dim, activation='relu')(encoder)
    decoder = Dense(input_dim, activation='tanh')(decoder)

    autoencoder = Model(inputs=input_layer, outputs=decoder)

    nb_epoch = 10
    batch_size = 64

    autoencoder.compile(optimizer='adam',
                        loss='mean_squared_error',
                        metrics=['accuracy'])

    autoencoder.fit(X_train, X_train, epochs=nb_epoch, batch_size=batch_size, shuffle=True,
                              validation_data=(x_test, x_test), verbose=1)

    autoencoder.save("model.h5")

    autoencoder = load_model('model.h5')

    return autoencoder


# https://www.linkedin.com/pulse/anomaly-detection-autoencoder-neural-network-applied-urls-daboubi/
def showloss(x_test, x_abnormal, model):
    # test
    x_concat = np.concatenate([x_test, x_abnormal], axis=0)
    losses = []
    for x in x_concat:
        # compute loss for each test sample
        x = np.expand_dims(x, axis=0)
        loss = model.test_on_batch(x, x)
        losses.append(loss[0])

    # plot
    fig, ax = plt.subplots()

    plt.plot(range(len(losses[:SAMPLES])), losses[:SAMPLES], linestyle='-', linewidth=1, label="normal image", color='blue')
    plt.plot(range(SAMPLES, len(losses)), losses[SAMPLES:], linestyle='-', linewidth=1, label="anomaly image", color='red')

    # create graph
    plt.legend(loc='best')
    plt.grid()
    plt.title("Reconstruction error for different classes")
    plt.ylabel("Reconstruction error")
    plt.xlabel("Data point index")

    # plt.savefig(args.result)
    # plt.clf()


def getThreasholdTrain(autoencoder, X, y_test):
    predictions = autoencoder.predict(X)
    mse = np.mean(np.power(X - predictions, 2), axis=1)

    threshold = np.quantile(mse, 0.9900)

    # showImage(X_test.values[101], predictions[101])
    error_df = pd.DataFrame(list(zip(list(mse.values.reshape(1, SAMPLES)[0]),
                                     list(y_test.values.reshape(1, SAMPLES)[0]))),
                            columns=['reconstruction_error', 'true_class'])
    y_pred = [1 if e > threshold else 0 for e in error_df.reconstruction_error.values]
    conf_matrix = confusion_matrix(error_df.true_class, y_pred)
    tn, fp, fn, tp = conf_matrix.ravel()
    print('TP:' + str(tp))
    print('FP:' + str(fp))
    print('TN:' + str(tn))
    print('FN:' + str(fn))
    accuracy = 1. * (tp + tn) / (tp + tn + fp + fn)

    groups = error_df.groupby('true_class')
    fig, ax = plt.subplots()

    for name, group in groups:
        ax.plot(group.index, group.reconstruction_error, marker='o', ms=2, linestyle='',
                label="Abnormal image" if name == 1 else "Normal image", color='red' if name == 1 else 'orange')
    ax.hlines(threshold, ax.get_xlim()[0], ax.get_xlim()[1], colors="green",
              zorder=100, label='Threshold=' + str(np.round(threshold, 3)))
    ax.legend()
    plt.title("Reconstruction error for different classes| Accuracy= " + str(accuracy))
    plt.ylabel("Reconstruction error")
    plt.xlabel("Data point index")

    return threshold


def showImage(x, pred_x):
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


def plotLoss(autoencoder, X_test, y_test, threshold):
    predictions = autoencoder.predict(X_test)
    mse = np.mean(np.power(X_test - predictions, 2), axis=1)

    # showImage(X_test.values[101], predictions[101])
    error_df = pd.DataFrame(list(zip(list(mse.values.reshape(1, SAMPLES + SAMPLES)[0]),
                                     list(y_test.values.reshape(1, SAMPLES + SAMPLES)[0]))),
                            columns=['reconstruction_error', 'true_class'])

    print('**************************')
    print('threshold', threshold)
    threshold += .0005
    y_pred = [1 if e > threshold else 0 for e in error_df.reconstruction_error.values]
    conf_matrix = confusion_matrix(error_df.true_class, y_pred)
    tn, fp, fn, tp = conf_matrix.ravel()
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
    fig, ax = plt.subplots()

    for name, group in groups:
        ax.plot(group.index, group.reconstruction_error, marker='o', ms=2, linestyle='',
                label="Abnormal image" if name == 1 else "Normal image", color='red' if name == 1 else 'orange')
    ax.hlines(threshold, ax.get_xlim()[0], ax.get_xlim()[1], colors="green",
              zorder=100, label='Threshold=' + str(np.round(threshold, 3)))
    ax.legend()
    plt.title("Reconstruction error for different classes| Accuracy= " + str(accuracy))
    plt.ylabel("Reconstruction error")
    plt.xlabel("Data point index")


def getThreashold(autoencoder, X_test, y_test, want_accuracy, want_recall):

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
        tn, fp, fn, tp = conf_matrix.ravel()
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
    fig, ax = plt.subplots()

    for name, group in groups:
        ax.plot(group.index, group.reconstruction_error, marker='o', ms=2, linestyle='',
                label="Abnormal image" if name == 1 else "Normal image", color='red' if name == 1 else 'orange')
    ax.hlines(threshold, ax.get_xlim()[0], ax.get_xlim()[1], colors="green",
              zorder=100, label='Threshold='+str(np.round(threshold,3)))
    ax.legend()
    plt.title("Reconstruction error for different classes| Accuracy= " + str(accuracy))
    plt.ylabel("Reconstruction error")
    plt.xlabel("Data point index")

    return threshold


def main():

    X_train, x_test, x_abnormal = getData()

    # model = getAutoencoderModel(X_train, x_test[:500])

    model = load_model('model.h5')

    threshold = getThreasholdTrain(model, pd.DataFrame(X_train[:SAMPLES]), pd.DataFrame([0 for _ in range(SAMPLES)]))

    showloss(x_test[:SAMPLES], x_abnormal[:SAMPLES], model)

    X_test = pd.DataFrame(np.concatenate([x_test[:SAMPLES], x_abnormal[:SAMPLES]], axis=0))
    Y_test = pd.DataFrame([0 for _ in range(SAMPLES)] + [1 for _ in range(SAMPLES)])

    # define the accuracy and recall
    want_accuracy, want_recall = 0.90, 0.5
    # getThreashold(model, X_test, Y_test, want_accuracy, want_recall)

    '''# shuffle the data
    data = np.hstack((X_test.values, Y_test.values))
    np.random.shuffle(data)
    data = pd.DataFrame(data)
    X_test = data.iloc[:, :-1]
    Y_test = data.iloc[:, -1]'''

    # threshold = getThreashold(model, X_test, Y_test, want_accuracy, want_recall)

    plotLoss(model, X_test, Y_test, threshold)

    print('\n\nThreshold', threshold)

    plt.show()

if __name__ == '__main__':
    main()