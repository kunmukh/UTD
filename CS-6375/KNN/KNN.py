# Kunal Mukherjee
# 2/16/2019
# CS 6375

# Import the libraries
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score
from scipy import stats


def KNN():
    # open an output file to write the result
    f = open("outputKNN.txt", "w")

    # load the data set
    spam_train = pd.read_csv("spam_train.data")
    spam_validate = pd.read_csv("spam_validation.data")
    spam_test = pd.read_csv("spam_test.data")

    # data processing, change label 0 to -1
    X_train = spam_train.drop('Y', axis=1)
    Y_train = spam_train['Y']
    Y_train = [-1 if i == 0 else i for i in Y_train]

    # calculate the mean and variance
    X_train_mean = np.asarray(X_train.mean())
    X_train_var = np.asarray(X_train.var())

    # convert the training to np array
    x_train = np.asarray(X_train)

    # normalize the data
    for i in range(x_train.shape[0]):
        for j in range(x_train.shape[1]):
            x_train[i][j] = (x_train[i][j] - X_train_mean[j]) / X_train_var[j]

    # convert the training data to np array
    y_train = np.asarray([np.float64(i) for i in Y_train])

    # data processing, change label 0 to -1
    X_validate = spam_validate.drop('Y', axis=1)
    Y_validate = spam_validate['Y']
    Y_validate = [-1 if i == 0 else i for i in Y_validate]

    # convert the validation data to np array
    x_validate = np.asarray(X_validate)

    # normalization of the validation data
    for i in range(x_validate.shape[0]):
        for j in range(x_validate.shape[1]):
            x_validate[i][j] = (x_validate[i][j] - X_train_mean[j]) / X_train_var[j]

    # convert the validation data to np array
    y_validate = np.asarray([np.float64(i) for i in Y_validate])

    k_list = [1, 5, 11, 15, 21]
    acc = 0
    k_best = 0

    # for each k
    for k in k_list:
        y_pred = []
        # make prediction on the validation data and find accuracy
        for x in x_validate:
            eucledian_dist = np.sum((x - x_train) ** 2, axis=1)
            k_nearest_x_train_ind = eucledian_dist.argsort()[:k]
            k_nearest_y_train = np.take(y_train, k_nearest_x_train_ind)
            y_pred.append(stats.mode(k_nearest_y_train)[0][0])

        y_pred = np.asarray(y_pred)
        print('k: ', k)
        print('Confusion Matrix: \n', confusion_matrix(y_validate, y_pred), '\n')
        print('Training Accuracy: ', accuracy_score(y_validate, y_pred), '\n\n')

        f.write('k: ' + str(k) + '\n')
        f.write('Confusion Matrix: \n' + str(confusion_matrix(y_validate, y_pred)) + '\n')
        f.write('Training Accuracy: ' + str(accuracy_score(y_validate, y_pred)) + '\n\n')

        # the k with the highest accuracy store that and use it on the testing data
        if accuracy_score(y_validate, y_pred) > acc:
            acc = accuracy_score(y_validate, y_pred)
            k_best = k

    # data processing, change label 0 to -1
    X_test = spam_test.drop('Y', axis=1)
    Y_test = spam_test['Y']
    Y_test = [-1 if i == 0 else i for i in Y_test]

    # convert the validation data to np array
    x_test = np.asarray(X_test)

    # normalize the data
    for i in range(x_test.shape[0]):
        for j in range(x_test.shape[1]):
            x_test[i][j] = (x_test[i][j] - X_train_mean[j]) / X_train_var[j]

    # convert the validation data to np array
    y_test = np.asarray([np.float64(i) for i in Y_test])

    # prediction lisy
    y_pred = []

    # using the best k, make predictions
    for x in x_test:
        eucledian_dist = np.sum((x - x_train) ** 2, axis=1)
        k_nearest_x_train_ind = eucledian_dist.argsort()[:k_best]
        k_nearest_y_train = np.take(y_train, k_nearest_x_train_ind)
        y_pred.append(stats.mode(k_nearest_y_train)[0][0])

    y_pred = np.asarray(y_pred)
    print('Best k: ', k_best)
    print('Confusion Matrix: \n', confusion_matrix(y_test, y_pred), '\n')
    print('Testing Accuracy: ', accuracy_score(y_test, y_pred), '\n\n')

    f.write('Best k: ' + str(k_best) + '\n')
    f.write('Confusion Matrix: \n' + str(confusion_matrix(y_test, y_pred)) + '\n')
    f.write('Testing Accuracy: ' + str(accuracy_score(y_test, y_pred)) + '\n\n')

    f.close()

def main():
    KNN()


if __name__ == '__main__':
    main()
